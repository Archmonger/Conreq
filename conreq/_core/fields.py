import contextlib

from django.db.models import FileField, OneToOneField, TextField, URLField
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.db.transaction import atomic
from django.forms import PasswordInput, ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy
from django_ace import AceWidget
from encrypted_fields.fields import EncryptedCharField

from conreq._core import forms, validators


class PythonTextField(TextField):
    """A regular TextField, but this one displays itself with a Python text editor."""

    def formfield(self, **kwargs):
        kwargs["widget"] = AceWidget(
            mode="python",
            width="100%",
            toolbar=False,
            showprintmargin=False,
        )
        return super().formfield(**kwargs)


class PasswordField(EncryptedCharField):
    """Encrypted character field that hides the user's input within the browser."""

    def formfield(self, **kwargs):
        if kwargs.get("widget"):
            kwargs["widget"] = kwargs["widget"](attrs={"type": "password"})
        else:
            kwargs["widget"] = PasswordInput(render_value=True)
        return super().formfield(**kwargs)


class HostnameOrURLField(URLField):
    """URL field that supports hostnames (ex. https://sonarr:8000)"""

    default_validators = [validators.HostnameOrURLValidator()]

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed twice.
        return super().formfield(
            **{
                "form_class": forms.HostnameOrURLField,
                **kwargs,
            }
        )


class URLOrRelativeURLField(URLField):
    """URL field that supports relative or absolute URLs
    (ex. /my/url/path or https://mydomain.com)"""

    default_validators = [validators.url_or_relative_url_validator]

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed twice.
        return super().formfield(
            **{
                "form_class": forms.URLOrRelativeURLField,
                **kwargs,
            }
        )


class AutoOneToOneField(OneToOneField):
    """
    A OneToOneField that automatically creates itself if it doesnt exist yet.
    Drop in replacement for a regular OneToOne field.

    Be mindful that the model that you use with this field must have default
    values for all required fields.

    Example:

    ```python
    class MyProfile(models.Model):
        user = AutoOneToOneField(User, primary_key=True)
        home_page = models.URLField(max_length=255, blank=True)
        icq = models.IntegerField(max_length=255, null=True)
    ```
    """

    def contribute_to_related_class(self, cls, related):
        setattr(
            cls,
            related.get_accessor_name(),
            _AutoSingleRelatedObjectDescriptor(related),
        )


class RestrictedFileField(FileField):
    """
    A FileField that allows certain restrictions.

        * content_types - List containing allowed content_types. Example: `['application/pdf', 'image/jpeg']`.
            See https://www.geeksforgeeks.org/http-headers-content-type/ for all content types.

        * max_upload_size - Number indicating the maximum bytes allowed for upload.
            2.5MB  (2621440)
            5MB    (5242880)
            10MB   (10485760)
            20MB   (20971520)
            50MB   (5242880)
            100M   (104857600)
            250MB  (214958080)
            500MB  (429916160)
    """

    def __init__(
        self,
        *args,
        content_types: list[str] | None = None,
        max_upload_size: int = 0,
        **kwargs,
    ):
        self.content_types = content_types
        self.max_upload_size = max_upload_size
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        file = data.file

        with contextlib.suppress(AttributeError):
            if self.content_types and file.content_type not in self.content_types:
                raise ValidationError(
                    gettext_lazy("Filetype not supported. Allowed filetypes: %s")
                    % ", ".join(map(str, self.content_types))
                )
            # pylint: disable=protected-access
            if self.max_upload_size and file._size > self.max_upload_size:
                raise ValidationError(
                    gettext_lazy("File size %s is larger than the maximum %s.")
                    % (filesizeformat(file._size), filesizeformat(self.max_upload_size))
                )
        return data


class _AutoSingleRelatedObjectDescriptor(ReverseOneToOneDescriptor):
    """
    The descriptor that handles the object creation for an AutoOneToOneField.
    """

    @atomic
    def __get__(self, instance, instance_type=None):
        model = getattr(self.related, "related_model", self.related.model)

        try:
            return super().__get__(instance, instance_type)
        except model.DoesNotExist:
            # Using get_or_create instead() of save() or create() as it better handles race conditions
            obj, _ = model.objects.get_or_create(**{self.related.field.name: instance})

            # Update Django's cache, otherwise first 2 calls to obj.relobj
            # will return 2 different in-memory objects
            self.related.set_cached_value(instance, obj)
            self.related.field.set_cached_value(obj, instance)
            return obj
