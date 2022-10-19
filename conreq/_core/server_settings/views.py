from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

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


@method_decorator(user_passes_test(lambda u: u.is_superuser), name="dispatch")
class GeneralSettingsView(SingletonUpdateView):
    form_class = GeneralSettingsForm
    model = GeneralSettings


@method_decorator(user_passes_test(lambda u: u.is_superuser), name="dispatch")
class StylingSettingsView(SingletonUpdateView):
    form_class = StylingSettingsForm
    model = StylingSettings


@method_decorator(user_passes_test(lambda u: u.is_superuser), name="dispatch")
class WebserverSettingsView(SingletonUpdateView):
    form_class = WebserverSettingsForm
    model = WebserverSettings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["success_message"] = "Restart for changes to take effect."
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name="dispatch")
class EmailSettingsView(SingletonUpdateView):
    form_class = EmailSettingsForm
    model = EmailSettings
