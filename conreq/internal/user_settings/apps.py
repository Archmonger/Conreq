from django.apps import AppConfig

from conreq.utils.modules import load


class ServerSettingsConfig(AppConfig):
    name = "conreq.internal.user_settings"
    verbose_name = "User Settings"

    def ready(self) -> None:
        load("components")
