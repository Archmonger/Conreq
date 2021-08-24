import functools
import os

from .generic import list_modules

PACKAGES_DIR = None
PACKAGES_DEV_DIR = None


def _load_dirs():
    """Need to load the packages from a different context to not cause exceptions on startup."""
    # pylint: disable=global-statement,import-outside-toplevel
    global PACKAGES_DIR, PACKAGES_DEV_DIR
    if not PACKAGES_DIR and not PACKAGES_DEV_DIR:
        from conreq import settings

        PACKAGES_DIR = getattr(settings, "PACKAGES_DIR")
        PACKAGES_DEV_DIR = getattr(settings, "PACKAGES_DEV_DIR")


_load_dirs()


@functools.cache
def list_packages() -> set[str]:
    """Returns a set of all Conreq packages."""
    return set(list_modules(PACKAGES_DIR) + list_modules(PACKAGES_DEV_DIR))


@functools.cache
def list_apps() -> set[str]:
    """Lists all Conreq apps within uster installed packages."""
    apps = set()
    user_packages = list_packages()
    for package in user_packages:
        apps_dir = os.path.join(PACKAGES_DIR, package, "apps")
        apps_dev_dir = os.path.join(PACKAGES_DEV_DIR, package, "apps")
        all_modules = list_modules(apps_dir) + list_modules(apps_dev_dir)
        for app in all_modules:
            apps.add(f"{package}.apps.{app}")
    return apps


@functools.cache
def list_apps_with(module_name: str) -> set[str]:
    """Iterates through all Conreq packages returns a list of apps that contain a specific module name."""
    apps_with = set()
    apps = list_apps()
    for app in apps:
        package, apps_dir, app_name = app.split(".")
        apps_dir = os.path.join(PACKAGES_DIR, package, apps_dir, app_name)
        apps_dev_dir = os.path.join(PACKAGES_DEV_DIR, package, apps_dir, app_name)
        all_modules = list_modules(apps_dir) + list_modules(apps_dev_dir)
        for module in all_modules:
            print(module)
            if module == module_name:
                apps_with.add(app)
    return apps_with
