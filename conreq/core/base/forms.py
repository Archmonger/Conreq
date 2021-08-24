from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import URLField

from . import validators


class HostnameOrURLField(URLField):
    """URL field that supports hostnames (ex. https://sonarr:8000)"""

    default_validators = [validators.ExtendedURLValidator()]


class InitializationForm(UserCreationForm):
    sonarr_url = HostnameOrURLField(max_length=255, required=False)
    sonarr_api_key = forms.CharField(max_length=255, required=False)
    radarr_url = HostnameOrURLField(max_length=255, required=False)
    radarr_api_key = forms.CharField(max_length=255, required=False)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")
