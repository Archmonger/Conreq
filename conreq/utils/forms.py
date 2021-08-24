from django.forms import URLField

from .validators import ExtendedURLValidator


class HostnameOrURLField(URLField):
    """URL field that supports hostnames (ex. https://sonarr:8000)"""

    default_validators = [ExtendedURLValidator()]
