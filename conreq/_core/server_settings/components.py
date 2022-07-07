from idom import component, html

from conreq import AuthLevel, config
from conreq._core.components import tabbed_viewport
from conreq._core.email.models import EmailSettings
from conreq._core.server_settings.forms import (
    EmailSettingsForm,
    GeneralSettingsForm,
    StylingSettingsForm,
    WebserverSettingsForm,
)
from conreq._core.server_settings.models import (
    GeneralSettings,
    StylingSettings,
    WebserverSettings,
)
from conreq._core.views import SingletonUpdateView
from conreq.utils.components import view_to_component


# TODO: Create generic notification agent API.
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["success_message"] = "Restart for changes to take effect."
        return context


@view_to_component(name="email_settings", auth_level=AuthLevel.admin)
class EmailSettingsView(SingletonUpdateView):
    form_class = EmailSettingsForm
    model = EmailSettings


def system_info(state, set_state):
    return html.div("Under Construction")


def licenses(state, set_state):
    return html.div("Under Construction")


# pylint: disable=protected-access
@component
def server_settings(state, set_state):
    return tabbed_viewport(
        state,
        set_state,
        tabs=config.tabs.server_settings.installed,
        top_tabs=config._internal_tabs.server_settings,
    )
