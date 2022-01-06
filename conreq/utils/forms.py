from django.forms import CharField, URLField

from conreq.utils.environment import get_env, set_env

from .validators import HostnameOrURLValidator


class HostnameOrURLField(URLField):
    """URL field that supports hostnames (ex. https://sonarr:8000)"""

    default_validators = [HostnameOrURLValidator()]


class EnvField:
    env_type = str

    def __init__(self, env_name, **kwargs) -> None:
        super().__init__(**kwargs)
        self.env_name = env_name

    def prepare_value(self, _):
        return get_env(self.env_name, return_type=self.env_type)


class EnvCharField(EnvField, CharField):
    pass


class EnvFormMixin:
    """Allows custom EnvFields for any ModelForm or Form.
    Forms will require calling `save()` to commit changes."""

    def save(self, commit: bool = True):
        super_class = super()
        saved = super().save(commit=commit) if getattr(super_class, "save") else None
        if commit:
            for name, field in self.base_fields.items():
                if isinstance(field, EnvField):
                    set_env(name, self.cleaned_data.get(name))

        return saved
