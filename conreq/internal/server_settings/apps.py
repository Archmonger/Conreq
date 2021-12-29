from django.apps import AppConfig

from conreq.utils.modules import load


class ServerSettingsConfig(AppConfig):
    name = "conreq.internal.server_settings"
    verbose_name = "Server"

    def ready(self) -> None:
        load("views")
