from django.forms import BooleanField, CharField, ChoiceField, IntegerField, URLField


from conreq.utils.environment import get_env, set_env

from . import validators, widgets


class HostnameOrURLField(URLField):
    """URL field that supports hostnames (ex. https://sonarr:8000)"""

    default_validators = [validators.HostnameOrURLValidator()]


class URLOrRelativeURLField(URLField):
    """URL field that supports relative or absolute URLs
    (ex. /my/url/path or https://mydomain.com)"""

    widget = widgets.URLOrRelativeURLInput
    default_validators = [validators.url_or_relative_url_validator]

    def to_python(self, value):
        value = super().to_python(value)
        if value and value.startswith("http:///"):
            # If value starts with ``http:///`` (followed by 3 slashes)
            # that means user provided a relative url and a parent ``URLField`` class
            # has appended a ``http://`` to it.
            # We need to strip it out and convert to correct relative url
            # before we pass it down the line.
            value = value[7:]
        return value


class EnvFieldMixin:
    """Generic field to read/write dot env values within a HTML form."""

    env_type = str

    def __init__(self, env_name, *, required=False, **kwargs) -> None:
        super().__init__(required=required, **kwargs)
        self.env_name = env_name

    def prepare_value(self, _):
        return get_env(
            self.env_name, default_value=self.initial, return_type=self.env_type
        )


class EnvCharField(EnvFieldMixin, CharField):
    """A character field that utilizes the env file, instead of the database."""


class EnvChoiceField(EnvFieldMixin, ChoiceField):
    """A choice field that utilizes the env file, instead of the database."""


class EnvBooleanField(EnvFieldMixin, BooleanField):
    """A boolean field that utilizes the env file, instead of the database."""

    env_type = bool


class EnvIntegerField(EnvFieldMixin, IntegerField):
    """An integer field that utilizes the env file, instead of the database."""

    env_type = int


class EnvFormMixin:
    """Allows custom EnvFields for any `ModelForm` or `Form`.

    `Form` will require calling `is_valid()` then `save()` to commit changes. This is
    done automatically if using `SaveFormViewMixin`."""

    def save(self, commit: bool = True):
        super_class = super()
        saved = (
            super().save(commit=commit) if getattr(super_class, "save", None) else None
        )
        if not commit:
            return saved

        for name, field in self.base_fields.items():
            if isinstance(field, EnvFieldMixin):
                set_env(field.env_name or name, self.cleaned_data.get(name))

        return saved
