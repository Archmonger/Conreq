from platform import platform

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django.conf import settings
from django.forms import CharField, Form, ModelForm

from conreq.internal.email.models import EmailSettings
from conreq.internal.server_settings.models import GeneralSettings, StylingSettings
from conreq.utils.forms import (
    EnvBooleanField,
    EnvCharField,
    EnvFormMixin,
    EnvIntegerField,
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


class WebserverSettingsForm(EnvFormMixin, Form):
    base_url = EnvCharField(
        env_name="BASE_URL",
        label="Base URL",
        max_length=255,
        help_text="Appears in all links (ex. example.com/base-url).",
    )
    host_ip_address = EnvCharField(
        env_name="WEBSERVER_HOST",
        label="Host IP",
        initial="0.0.0.0",
        help_text="Host address to bind to. '0.0.0.0' is all hosts.",
    )
    port = EnvIntegerField(
        env_name="WEBSERVER_PORT",
        initial=8000,
        help_text="Port number to bind to.",
    )
    rotate_secret_key = EnvBooleanField(
        env_name="ROTATE_SECRET_KEY",
        initial=False,
        help_text="Invalidates user sessions upon server restart.",
    )
    workers = EnvIntegerField(
        env_name="WEBSERVER_WORKERS",
        initial=3,
        help_text="Number of worker processes for the webserver to use.",
    )
    ssl_ca_certificate = EnvCharField(
        env_name="WEBSERVER_CA_CERTS",
        label="SSL CA certificate",
        help_text="Path to the SSL CA certificate file.",
    )
    ssl_certificate = EnvCharField(
        env_name="WEBSERVER_CERTFILE",
        label="SSL certificate",
        help_text="Path to the SSL certificate file.",
    )
    ssl_key = EnvCharField(
        env_name="WEBSERVER_KEYFILE",
        label="SSL key",
        help_text="Path to the SSL key file.",
    )
    quic_host_ip_address = EnvCharField(
        env_name="WEBSERVER_QUIC_HOST",
        label="QUIC host IP address",
        initial="",
        help_text="Host address to bind QUIC to. '0.0.0.0' is all hosts.",
    )
    quic_port = EnvIntegerField(
        env_name="WEBSERVER_QUIC_PORT",
        label="QUIC port",
        help_text="Port number to bind QUIC to.",
    )
    debug = EnvBooleanField(
        env_name="WEBSERVER_DEBUG",
        help_text="Enable extra webserver logging and checks.",
    )

    class Meta:
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
