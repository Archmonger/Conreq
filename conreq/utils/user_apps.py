import os
from importlib import import_module

from django.conf import settings

from .generic import list_modules

APPS_DIR = getattr(settings, "APPS_DIR")


def list_user_apps() -> list[str]:
    apps_list = []
    user_apps = list_modules(APPS_DIR)
    for user_app in user_apps:
        package_dict = {}
        package_dict["name"] = user_app
        package_dict["modules"] = {}
        app_dir = os.path.join(APPS_DIR, user_app)
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


def list_user_apps_with(submodule_name: str) -> list[str]:
    apps_list = []
    user_apps = list_modules(APPS_DIR)
    for user_app in user_apps:
        app_dir = os.path.join(APPS_DIR, user_app)
        for package in list_modules(app_dir):
            sub_app_dir = os.path.join(app_dir, package)
            modules = list_modules(sub_app_dir)
            if submodule_name in modules:
                apps_list.append(user_app + "." + package + "." + submodule_name)
    return apps_list
