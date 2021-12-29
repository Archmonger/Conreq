from conreq import config
from conreq.app import register
from conreq.internal.email.models import EmailSettings
from conreq.internal.server_settings.forms import (
    EmailSettingsForm,
    GeneralSettingsForm,
    StylingSettingsForm,
    WebserverSettingsForm,
)
from conreq.internal.server_settings.models import (
    GeneralSettings,
    StylingSettings,
    WebserverSettings,
)
from conreq.utils.components import django_to_idom, tabbed_viewport
from conreq.utils.views import SingletonUpdateView


@register.tabs.server_settings("General")
@django_to_idom()
class GeneralSettingsView(SingletonUpdateView):
    form_class = GeneralSettingsForm
    model = GeneralSettings


@register.tabs.server_settings("Styling")
@django_to_idom()
class StylingSettingsView(SingletonUpdateView):
    form_class = StylingSettingsForm
    model = StylingSettings


@register.tabs.server_settings("Webserver")
@django_to_idom()
class WebserverSettingsView(SingletonUpdateView):
    form_class = WebserverSettingsForm
    model = WebserverSettings


@register.tabs.server_settings("Email")
@django_to_idom()
class EmailSettingsView(SingletonUpdateView):
    form_class = EmailSettingsForm
    model = EmailSettings


@register.homepage.nav_tab("Server Settings", "Admin")
@register.component.server_settings()
def server_settings(websocket, viewport_state, set_viewport_state):
    return tabbed_viewport(websocket, config.tabs.server_settings)
