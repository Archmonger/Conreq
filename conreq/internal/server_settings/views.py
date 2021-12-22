from conreq.internal.server_settings.forms import (
    GeneralSettingsForm,
    StylingSettingsForm,
    WebserverSettingsForm,
)
from conreq.internal.server_settings.models import (
    GeneralSettings,
    StylingSettings,
    WebserverSettings,
)
from conreq.utils.views import SingletonUpdateView

# TODO: Tabs for general, styling, webserver, and email


class GeneralSettingsView(SingletonUpdateView):
    form_class = GeneralSettingsForm
    model = GeneralSettings


class StylingSettingsView(SingletonUpdateView):
    form_class = StylingSettingsForm
    model = StylingSettings


class WebserverSettingsView(SingletonUpdateView):
    form_class = WebserverSettingsForm
    model = WebserverSettings


def server_settings(request):
    return StylingSettingsView.as_view()(request)
