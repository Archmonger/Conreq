from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from conreq.utils.fields import HostnameOrURLField


class InitializationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")
