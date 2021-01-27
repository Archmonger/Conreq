from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class initializationForm(UserCreationForm):
    sonarr_url = forms.URLField(required=False)
    sonarr_api_key = forms.CharField(max_length=50, required=False)
    radarr_url = forms.URLField(required=False)
    radarr_api_key = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
