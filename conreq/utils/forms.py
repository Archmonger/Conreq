from django.forms import BooleanField, CharField, ChoiceField, IntegerField, URLField

from conreq.utils.environment import get_env, set_env

from .validators import HostnameOrURLValidator


class HostnameOrURLField(URLField):
    """URL field that supports hostnames (ex. https://sonarr:8000)"""

    default_validators = [HostnameOrURLValidator()]


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
