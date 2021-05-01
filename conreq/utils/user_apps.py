from conreq.settings import APPS_DIR
from .generic import list_modules
import os


def list_user_apps():
    apps_list = []
    user_apps = list_modules(APPS_DIR)
    for user_app in user_apps:
        package_dict = {}
        package_dict["name"] = user_app
        package_dict["modules"] = {}
        app_dir = os.path.join(APPS_DIR, user_app)
        for package in list_modules(app_dir):
            sub_app_dir = os.path.join(app_dir, package)
            package_dict["modules"][package] = []
            for module in list_modules(sub_app_dir):
                package_dict["modules"][package].append(
                    (module, user_app + "." + package + "." + module)
                )
        apps_list.append(package_dict)

    return apps_list
