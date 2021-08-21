import functools
import os
from importlib import import_module

from django.conf import settings

from .generic import list_modules

PACKAGES_DIR = getattr(settings, "PACKAGES_DIR")


@functools.cache
def list_apps() -> list[str]:
    """Lists all Conreq apps within uster installed packages."""
    apps_list = []
    user_apps = list_modules(PACKAGES_DIR)
    for user_app in user_apps:
        package_dict = {}
        package_dict["name"] = user_app
        package_dict["modules"] = {}
        app_dir = os.path.join(PACKAGES_DIR, user_app)
        for package in list_modules(app_dir):
            sub_app_dir = os.path.join(app_dir, package)
            if package == "settings":
                module = import_module(user_app + "." + package)
                package_dict["settings"] = [
                    item for item in dir(module) if not item.startswith("_")
                ]
            else:
                package_dict["modules"][package] = []
                for module in list_modules(sub_app_dir):
                    package_dict["modules"][package].append(
                        (module, user_app + "." + package + "." + module)
                    )
        apps_list.append(package_dict)

    return apps_list


@functools.cache
def list_apps_with(submodule_name: str) -> list[str]:
    """Iterates through all Conreq apps within user installed packages and returns a list of apps that contain a specific module name."""
    apps_list = []
    user_apps = list_modules(PACKAGES_DIR)
    for user_app in user_apps:
        app_dir = os.path.join(PACKAGES_DIR, user_app)
        for package in list_modules(app_dir):
            sub_app_dir = os.path.join(app_dir, package)
            modules = list_modules(sub_app_dir)
            if submodule_name in modules:
                apps_list.append(user_app + "." + package + "." + submodule_name)
    return apps_list
