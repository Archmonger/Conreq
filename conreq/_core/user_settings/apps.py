from django.apps import AppConfig

from conreq.utils.modules import load


class ServerSettingsConfig(AppConfig):
    name = "conreq._core.user_settings"
    verbose_name = "User Settings"

    def ready(self):
        load("components")
