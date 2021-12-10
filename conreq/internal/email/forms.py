from django import forms

from .models import EmailConfig


class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailConfig
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }
