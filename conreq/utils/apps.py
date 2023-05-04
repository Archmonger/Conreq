import importlib
import os

from conreq.utils.generic import remove_duplicates_from_list
from conreq.utils.modules import _find_wildcards, find_modules
from conreq.utils.packages import _packages_dev_dir, _packages_dir, find_packages


def find_apps() -> set[str]:
    """Returns all apps within installed packages. Apps must be declared
    within a package's `django_apps` list. If the delcared app contains a
    trailing wildcard, all modules within the given directory are considered apps."""
    apps = set()
    user_packages = find_packages()

    for package in user_packages:
        module = importlib.import_module(package)
        if hasattr(module, "django_apps") and isinstance(module.django_apps, list):
            for app in module.django_apps:
                if app.endswith(".*"):
                    apps.update(_find_wildcards(app))
                else:
                    apps.add(app)
    return apps


def find_apps_with(module_name: str) -> set[str]:
    """Returns all Conreq apps that contain a specific module name."""
    apps_with = set()
    apps = find_apps()

    for app in apps:
        package, apps_dir, app_name = app.split(".")
        apps_dir = os.path.join(_packages_dir(), package, apps_dir, app_name)
        apps_dev_dir = os.path.join(_packages_dev_dir(), package, apps_dir, app_name)
        all_modules = find_modules(apps_dir) + find_modules(apps_dev_dir)
        all_modules = remove_duplicates_from_list(all_modules)
        for module in all_modules:
            if module == module_name:
                apps_with.add(app)

    return apps_with
