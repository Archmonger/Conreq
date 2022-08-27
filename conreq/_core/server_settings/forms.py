from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.conf import settings
from django.db.models import TextChoices
from django.forms import CharField, ModelForm
from django_ace import AceWidget

from conreq._core.email.models import EmailSettings
from conreq._core.forms import (
    EnvBooleanField,
    EnvCharField,
    EnvChoiceField,
    EnvFormMixin,
    EnvIntegerField,
)
from conreq._core.server_settings.models import (
    GeneralSettings,
    StylingSettings,
    WebserverSettings,
)
from conreq.utils.environment import get_home_url


class LogLevelChoices(TextChoices):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class GeneralSettingsForm(EnvFormMixin, ModelForm):
    debug_mode = EnvBooleanField(
        env_name="DEBUG_MODE",
        initial=settings.DEBUG,
        help_text="Disables security features and adds debugging tools.",
    )
    safe_mode = EnvBooleanField(
        env_name="SAFE_MODE",
        help_text="Disables all installed apps.",
    )
    logging_level = EnvChoiceField(
        env_name="LOG_LEVEL",
        initial=settings.LOG_LEVEL,
        choices=LogLevelChoices.choices,
    )

    class Meta:
        model = GeneralSettings
        fields = (
            "server_name",
            "server_description",
            "public_url",
            "app_store_url",
            "logging_level",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


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
    # Remember to change the default in settings.py if you change these defaults
    base_url = EnvCharField(
        env_name="BASE_URL",
        label="Base URL",
        help_text='Appears in all links. A value of "base-url" will result in example.com/base-url.',
    )
    home_url = EnvCharField(
        env_name="HOME_URL",
        label="Home URL",
        initial=get_home_url(False, False),
        required=True,
        help_text='Appears in homepage links. A value of "home-url" will result in example.com/base-url/home-url.',
    )
    session_max_age = EnvIntegerField(
        env_name="SESSION_COOKIE_AGE",
        initial=settings.SESSION_COOKIE_AGE,
        required=True,
        help_text="Maximum time in seconds for a user session to last.",
    )
    secure_referrer_policy = EnvChoiceField(
        env_name="SECURE_REFERRER_POLICY",
        initial=ReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN,
        choices=ReferrerPolicy.choices,
        required=True,
        help_text="The HTTP referrer policy to apply.",
    )
    allowed_hosts = EnvCharField(
        env_name="ALLOWED_HOSTS",
        initial=", ".join(settings.ALLOWED_HOSTS),
        required=True,
        help_text="Comma separated list of IPs or domains the webserver is allowed to \
            serve (ex. example.com, 127.0.0.1). Wildcards (*) are allowed within the URLs.",
    )
    allowed_forwarding_ips = EnvCharField(
        env_name="ALLOWED_FORWARDING_IPS",
        label="Allowed forwarding IPs",
        initial=", ".join(settings.ALLOWED_FORWARDING_IPS),
        required=False,
        help_text="Comma separated list of IPs to trust with reverse proxy headers \
            (ex. 192.168.86.25, 10.0.0.51).",
    )
    csrf_trusted_origins = EnvCharField(
        env_name="CSRF_TRUSTED_ORIGINS",
        label="CSRF trusted origins",
        initial=", ".join(settings.CSRF_TRUSTED_ORIGINS),
        help_text='Comma separated list of <b>qualified</b> URLs trusted for \
            <a href="https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html">\
                CSRF protection</a> (ex. https://example.com). Wildcards (*) are allowed within the URLs. <br> If this field \
                    is empty, URLs will be automatically generated based on "Allowed Domains".',
    )
    rotate_secret_key = EnvBooleanField(
        env_name="ROTATE_SECRET_KEY",
        help_text="Invalidates user sessions upon every server restart.",
    )
    host_ip = EnvCharField(
        env_name="HOST_IP",
        label="Host IP",
        initial="0.0.0.0",
        required=True,
        help_text="Networking address to bind to. For all hosts, use 0.0.0.0",
    )
    host_port = EnvIntegerField(
        env_name="HOST_PORT",
        initial=7575,
        max_value=65535,
        required=True,
        help_text="Port number to bind to.",
    )
    worker_processes = EnvIntegerField(
        env_name="WEBSERVER_WORKERS",
        initial=settings.WEBSERVER_WORKERS,
        required=True,
        help_text="Number of separate worker processes for the webserver to use. <b>Each worker uses approximately 80MB additional memory.</b>",
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
            "host_ip",
            "host_port",
            "session_max_age",
            "rotate_secret_key",
            "secure_referrer_policy",
            "allowed_hosts",
            "allowed_forwarding_ips",
            "csrf_trusted_origins",
            "worker_processes",
            "ssl_certificate",
            "ssl_key",
            "ssl_ca_certificate",
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
