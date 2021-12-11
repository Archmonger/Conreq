from django.forms import URLField

from .validators import HostnameOrURLValidator


class HostnameOrURLField(URLField):
    """URL field that supports hostnames (ex. https://sonarr:8000)"""

    default_validators = [HostnameOrURLValidator()]
