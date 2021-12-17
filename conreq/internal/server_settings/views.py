from django.views.generic.edit import UpdateView

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


class SettingsViewMixin:
    template_name = "conreq/simple_form.html"

    def get_success_url(self):
        self.success_url = self.request.path
        return super().get_success_url()

    def get_object(self, queryset=None):
        return self.model.get_solo()


class GeneralSettingsView(SettingsViewMixin, UpdateView):
    form_class = GeneralSettingsForm
    model = GeneralSettings


class StylingSettingsView(SettingsViewMixin, UpdateView):
    form_class = StylingSettingsForm
    model = StylingSettings


class WebserverSettingsView(SettingsViewMixin, UpdateView):
    form_class = WebserverSettingsForm
    model = WebserverSettings


def server_settings(request):
    return StylingSettingsView.as_view()(request)
