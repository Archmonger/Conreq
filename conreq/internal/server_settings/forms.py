from platform import platform

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django.conf import settings
from django.db.models import TextChoices
from django.forms import CharField, ModelForm

from conreq.internal.email.models import EmailSettings
from conreq.internal.server_settings.models import (
    GeneralSettings,
    StylingSettings,
    WebserverSettings,
)
from conreq.utils.environment import get_home_url
from conreq.utils.forms import (
    EnvBooleanField,
    EnvCharField,
    EnvChoiceField,
    EnvFormMixin,
    EnvIntegerField,
)


class GeneralSettingsForm(EnvFormMixin, ModelForm):
    debug_mode = EnvBooleanField(
        initial=settings.DEBUG,
        help_text="Disables security features and adds debugging tools. Restart for this change to take effect.",
    )
    safe_mode = EnvBooleanField(
        initial=settings.SAFE_MODE,
        help_text="Disables all installed apps. Restart for this change to take effect.",
    )
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


class ReferrerPolicy(TextChoices):
    NO_REFERRER = "no-referrer"
    NO_REFERRER_WHEN_DOWNGRADE = "no-referrer-when-downgrade"
    ORIGIN = "origin"
    ORIGIN_WHEN_CROSS_ORIGIN = "origin-when-cross-origin"
    SAME_ORIGIN = "same-origin"
    STRICT_ORIGIN = "strict-origin"
    STRICT_ORIGIN_WHEN_CROSS_ORIGIN = "strict-origin-when-cross-origin"
    UNSAFE_URL = "unsafe-url"


# TODO: Set these initial values based on settings.py
class WebserverSettingsForm(EnvFormMixin, ModelForm):
    base_url = EnvCharField(
        label="Base URL",
        help_text="Appears in all links. A value of 'base-url' will result in example.com/base-url.",
    )
    home_url = EnvCharField(
        label="Home URL",
        initial=get_home_url(False, False),
        help_text="A value of 'my-home-url' will result in example.com/base-url/home-url.",
    )
    secure_referrer_policy = EnvChoiceField(
        initial=ReferrerPolicy.NO_REFERRER,
        choices=ReferrerPolicy.choices,
        help_text="The HTTP referrer policy to apply.",
    )
    if len(settings.ALLOWED_HOSTS) == 1:
        allowed_domain = EnvCharField(
            initial=settings.ALLOWED_HOSTS[0],
            help_text="The IP Address or web domain the webserver is allowed to serve (ex. example.com). To allow all, use an asterisk (*).",
        )
    rotate_secret_key = EnvBooleanField(
        env_name="ROTATE_SECRET_KEY",
        help_text="Invalidates user sessions upon server restart.",
    )
    host_ip = EnvCharField(
        env_name="WEBSERVER_HOST",
        label="Host IP",
        initial="0.0.0.0",
        help_text="Networking address to bind to. For all hosts, use 0.0.0.0.",
    )
    host_port = EnvIntegerField(
        env_name="WEBSERVER_PORT",
        initial=8000,
        max_value=65535,
        help_text="Port number to bind to.",
    )
    quic_host_ip = EnvCharField(
        env_name="WEBSERVER_QUIC_HOST",
        label="QUIC host IP address",
        initial="",
        help_text="Host address to bind QUIC to. '0.0.0.0' is all hosts.",
    )
    quic_host_port = EnvIntegerField(
        env_name="WEBSERVER_QUIC_PORT",
        label="QUIC port",
        max_value=65535,
        help_text="Port number to bind QUIC to.",
    )
    workers = EnvIntegerField(
        env_name="WEBSERVER_WORKERS",
        initial=settings.WEBSERVER_WORKERS,
        help_text="Number of worker processes for the webserver to use. Each worker uses additional memory.",
    )
    webserver_debug = EnvBooleanField(
        env_name="WEBSERVER_DEBUG",
        help_text="Enable extra webserver logging and checks.",
    )

    class Meta:
        model = WebserverSettings
        fields = [
            "base_url",
            "home_url",
            "secure_referrer_policy",
            "allowed_domain",
            "rotate_secret_key",
            "host_ip",
            "host_port",
            "quic_host_ip",
            "quic_host_port",
            "workers",
            "ssl_ca_certificate",
            "ssl_certificate",
            "ssl_key",
            "webserver_debug",
        ]

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
