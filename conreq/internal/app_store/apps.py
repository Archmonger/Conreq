from django.apps import AppConfig

MODULE = __name__
APP = MODULE[: MODULE.rfind(".")]


class AppStoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = APP
    verbose_name = "App Store"
