from django.apps import AppConfig, apps

from conreq.utils.modules import autoload_modules


class AppLoaderConfig(AppConfig):
    name = "conreq.internal.app_loader"

    def ready(self):
        for app_config in apps.get_app_configs():
            autoload_modules(app_config)
