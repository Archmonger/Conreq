import functools
import os

from conreq.utils import log

from .generic import list_modules

_logger = log.get_logger(__name__)


@functools.cache
def _packages_dir():
    """Load the packages dir from a different context to avoid circular imports."""
    # pylint: disable=import-outside-toplevel
    from conreq import settings

    return getattr(settings, "PACKAGES_DIR")


@functools.cache
def _packages_dev_dir():
    """Load the dev packages dir from a different context to not cause exceptions on startup."""
    # pylint: disable=import-outside-toplevel
    from conreq import settings

    return getattr(settings, "PACKAGES_DEV_DIR")


def _duplicate_package_check(packages):
    seen = set()
    for package in packages:
        if package in seen:
            log.handler(
                f"Using development copy of duplicate package '{package}'",
                log.WARNING,
                _logger,
            )
        seen.add(package)


@functools.cache
def list_packages() -> set[str]:
    """Returns all Conreq packages."""
    packages = list_modules(_packages_dir()) + list_modules(_packages_dev_dir())
    _duplicate_package_check(packages)
    return set(packages)


@functools.cache
def list_apps() -> set[str]:
    """Returns all Conreq apps within packages."""
    apps = set()
    user_packages = list_packages()
    for package in user_packages:
        apps_dir = os.path.join(_packages_dir(), package, "apps")
        apps_dev_dir = os.path.join(_packages_dev_dir(), package, "apps")
        all_modules = list_modules(apps_dir) + list_modules(apps_dev_dir)
        for app in all_modules:
            apps.add(f"{package}.apps.{app}")
    return apps


@functools.cache
def list_apps_with(module_name: str) -> set[str]:
    """Returns all Conreq apps that contain a specific module name."""
    apps_with = set()
    apps = list_apps()
    for app in apps:
        package, apps_dir, app_name = app.split(".")
        apps_dir = os.path.join(_packages_dir(), package, apps_dir, app_name)
        apps_dev_dir = os.path.join(_packages_dev_dir(), package, apps_dir, app_name)
        all_modules = list_modules(apps_dir) + list_modules(apps_dev_dir)
        for module in all_modules:
            print(module)
            if module == module_name:
                apps_with.add(app)
    return apps_with
