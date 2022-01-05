from platform import platform

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django.conf import settings
from django.forms import CharField, ModelForm

from conreq.internal.email.models import EmailSettings
from conreq.internal.server_settings.models import (
    GeneralSettings,
    StylingSettings,
    WebserverSettings,
)


class GeneralSettingsForm(ModelForm):
    conreq_version = CharField(
        initial=settings.CONREQ_VERSION, disabled=True, required=False
    )
    system_platform = CharField(initial=platform(), disabled=True, required=False)

    class Meta:
        model = GeneralSettings
        fields = ("server_name", "server_description", "app_store_url")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))
        self.helper.add_input(Button("clear-cache", "Clear Cache"))


class StylingSettingsForm(ModelForm):
    class Meta:
        model = StylingSettings
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


class WebserverSettingsForm(ModelForm):
    base_url = CharField(
        required=False,
        max_length=255,
        help_text="Appears in all links (ex. example.com/base-url).",
    )

    class Meta:
        model = WebserverSettings
        fields = ["base_url", "rotate_secret_key"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


class EmailSettingsForm(ModelForm):
    class Meta:
        model = EmailSettings
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))
