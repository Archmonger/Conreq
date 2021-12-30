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

# pylint: disable=protected-access


@django_to_idom()
class GeneralSettingsView(SingletonUpdateView):
    form_class = GeneralSettingsForm
    model = GeneralSettings


@django_to_idom()
class StylingSettingsView(SingletonUpdateView):
    form_class = StylingSettingsForm
    model = StylingSettings


@django_to_idom()
class WebserverSettingsView(SingletonUpdateView):
    form_class = WebserverSettingsForm
    model = WebserverSettings


@django_to_idom()
class EmailSettingsView(SingletonUpdateView):
    form_class = EmailSettingsForm
    model = EmailSettings


@register.homepage.nav_tab("Server Settings", "Admin")
@register.component.server_settings()
def server_settings(websocket, state, set_state):
    return tabbed_viewport(
        websocket,
        state,
        set_state,
        tabs=config.tabs.server_settings,
        top_tabs=config._tabs.server_settings,
    )


# Set the internal tabs
config._tabs.server_settings["General"] = {"component": GeneralSettingsView}
config._tabs.server_settings["Styling"] = {"component": StylingSettingsView}
config._tabs.server_settings["Webserver"] = {"component": WebserverSettingsView}
config._tabs.server_settings["Email"] = {"component": EmailSettingsView}
