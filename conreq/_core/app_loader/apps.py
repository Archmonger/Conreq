import pkgutil
from importlib import import_module

from django.apps import AppConfig, apps


class AppLoaderConfig(AppConfig):
    name = "conreq._core.app_loader"
    skip_module_names = {
        "admin",
        "apps",
        "migrations",
        "templatetags",
        "management",
    }

    def ready(self):
        for app_config in apps.get_app_configs():
            self.auto_import_all(app_config)

    def auto_import_all(self, app_config: AppConfig):
        """Imports all submodules for a specific app."""
        if not getattr(app_config, "auto_import", False):
            return

        fail_silently = getattr(app_config, "auto_import_silent", False)

        for loader, module_name, is_pkg in pkgutil.walk_packages([app_config.path]):
            try:
                if module_name not in self.skip_module_names:
                    import_module(".".join([app_config.name, module_name]))
                    if is_pkg:
                        loader.find_module(module_name).load_module(module_name)  # type: ignore
            except Exception as exception:
                if not fail_silently:
                    raise exception
