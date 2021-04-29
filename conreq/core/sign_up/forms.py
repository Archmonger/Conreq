from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")