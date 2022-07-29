from django.apps import AppConfig

from conreq.utils.modules import load


class ServerSettingsConfig(AppConfig):
    name = "conreq._core.server_settings"
    verbose_name = "Server"

    def ready(self):
        load("components")
