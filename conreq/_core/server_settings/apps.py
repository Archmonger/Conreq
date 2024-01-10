from django.apps import AppConfig
from reactpy_django.utils import register_iframe

from conreq.utils.modules import load


class ServerSettingsConfig(AppConfig):
    name = "conreq._core.server_settings"
    verbose_name = "Server"

    def ready(self):
        from . import views

        load("components")
        register_iframe(views.GeneralSettingsView)
        register_iframe(views.StylingSettingsView)
        register_iframe(views.WebserverSettingsView)
        register_iframe(views.EmailSettingsView)
