from django.apps import AppConfig

from conreq.utils.modules import load

MODULE = __name__
APP = MODULE[: MODULE.rfind(".")]


class AppStoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = APP
    verbose_name = "App Store"

    def ready(self) -> None:
        load("views")
