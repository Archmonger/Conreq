from conreq import AuthLevel, config
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
from conreq.internal.utils import tab_constructor
from conreq.utils.components import tabbed_viewport, view_to_component
from conreq.utils.views import SingletonUpdateView


@view_to_component(name="general_settings", auth_level=AuthLevel.admin)
class GeneralSettingsView(SingletonUpdateView):
    form_class = GeneralSettingsForm
    model = GeneralSettings


@view_to_component(name="styling_settings", auth_level=AuthLevel.admin)
class StylingSettingsView(SingletonUpdateView):
    form_class = StylingSettingsForm
    model = StylingSettings


@view_to_component(name="webserver_settings", auth_level=AuthLevel.admin)
class WebserverSettingsView(SingletonUpdateView):
    form_class = WebserverSettingsForm
    model = WebserverSettings


@view_to_component(name="email_settings", auth_level=AuthLevel.admin)
class EmailSettingsView(SingletonUpdateView):
    form_class = EmailSettingsForm
    model = EmailSettings


@register.component.server_settings()
def server_settings(websocket, state, set_state):
    return tabbed_viewport(
        websocket,
        state,
        set_state,
        tabs=config.tabs.server_settings,
        top_tabs=config._tabs.server_settings,
    )


# pylint: disable=protected-access
# Set the internal tabs
config._tabs.server_settings["General"] = {"component": GeneralSettingsView}
config._tabs.server_settings["Styling"] = {"component": StylingSettingsView}
config._tabs.server_settings["Webserver"] = {"component": WebserverSettingsView}
config._tabs.server_settings["Email"] = {"component": EmailSettingsView}
config._homepage.admin_nav_tabs[2] = tab_constructor("Server Settings", server_settings)
