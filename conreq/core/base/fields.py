from django.db.models import URLField

from . import forms, validators


class HostnameOrURLField(URLField):
    """URL field that supports hostnames (ex. https://sonarr:8000)"""

    default_validators = [validators.ExtendedURLValidator()]

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed
        # twice.
        return super().formfield(
            **{
                "form_class": forms.HostnameOrURLField,
                **kwargs,
            }
        )
