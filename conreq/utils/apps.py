import os

from conreq.utils.generic import remove_duplicates_from_list
from conreq.utils.packages import (
    _packages_dev_dir,
    _packages_dir,
    find_modules,
    find_packages,
)


def find_apps() -> set[str]:
    """Returns all Conreq apps within any installed packages."""
    apps = set()
    user_packages = find_packages()

    for package in user_packages:
        apps_dir = os.path.join(_packages_dir(), package, "apps")
        apps_dev_dir = os.path.join(_packages_dev_dir(), package, "apps")
        all_modules = find_modules(apps_dir) + find_modules(apps_dev_dir)
        all_modules = remove_duplicates_from_list(all_modules)
        for app in all_modules:
            apps.add(f"{package}.apps.{app}")

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
