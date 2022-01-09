from platform import platform

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django.conf import settings
from django.db.models import TextChoices
from django.forms import CharField, ModelForm
from django_ace import AceWidget

from conreq._core.email.models import EmailSettings
from conreq._core.server_settings.models import (
    GeneralSettings,
    StylingSettings,
    WebserverSettings,
)
from conreq.app.forms import (
    EnvBooleanField,
    EnvCharField,
    EnvChoiceField,
    EnvFormMixin,
    EnvIntegerField,
)
from conreq.utils.environment import get_home_url


class GeneralSettingsForm(EnvFormMixin, ModelForm):
    session_max_age = EnvIntegerField(
        env_name="SESSION_COOKIE_AGE",
        initial=settings.SESSION_COOKIE_AGE,
        help_text="Maximum time in seconds for a user session to last. <b>Restart for this change to take effect.</b>",
    )
    debug_mode = EnvBooleanField(
        env_name="DEBUG_MODE",
        initial=settings.DEBUG,
        help_text="Disables security features and adds debugging tools. <b>Restart for this change to take effect.</b>",
    )
    safe_mode = EnvBooleanField(
        env_name="SAFE_MODE",
        initial=settings.SAFE_MODE,
        help_text="Disables all installed apps. <b>Restart for this change to take effect.</b>",
    )
    conreq_version = CharField(
        initial=settings.CONREQ_VERSION, disabled=True, required=False
    )
    system_platform = CharField(initial=platform(), disabled=True, required=False)

    class Meta:
        model = GeneralSettings
        fields = ("server_name", "server_description", "public_url", "app_store_url")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))
        self.helper.add_input(Button("clear-cache", "Clear Cache"))


class StylingSettingsForm(ModelForm):
    head_html = CharField(
        widget=AceWidget(
            mode="html",
            theme="twilight",
            width="100%",
            toolbar=False,
            showprintmargin=False,
        ),
        label="Custom HTML (head)",
        required=False,
    )

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
        env_name="BASE_URL",
        label="Base URL",
        help_text="Appears in all links. A value of 'base-url' will result in example.com/base-url.",
    )
    home_url = EnvCharField(
        env_name="HOME_URL",
        label="Home URL",
        initial=get_home_url(False, False),
        help_text="A value of 'home-url' will result in example.com/base-url/home-url.",
    )
    secure_referrer_policy = EnvChoiceField(
        env_name="SECURE_REFERRER_POLICY",
        initial=ReferrerPolicy.NO_REFERRER,
        choices=ReferrerPolicy.choices,
        help_text="The HTTP referrer policy to apply.",
    )
    if len(settings.ALLOWED_HOSTS) == 1:
        allowed_domain = EnvCharField(
            env_name="ALLOWED_HOST",
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
    worker_processes = EnvIntegerField(
        env_name="WEBSERVER_WORKERS",
        initial=settings.WEBSERVER_WORKERS,
        help_text="Number of separate worker processes for the webserver to use. <b>Each worker uses additional memory.</b>",
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
            "worker_processes",
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
