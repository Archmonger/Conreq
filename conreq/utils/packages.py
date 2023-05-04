import functools
import importlib
import logging

from conreq.utils.generic import list_intersection, remove_duplicates_from_list
from conreq.utils.modules import find_modules

_logger = logging.getLogger(__name__)


def find_packages() -> list[str]:
    """Returns all Conreq packages."""
    packages = find_modules(_packages_dir())
    packages_dev = find_modules(_packages_dev_dir())
    _duplicate_package_warning(packages, packages_dev)
    clean_packages = remove_duplicates_from_list(packages + packages_dev)
    clean_packages = _remove_invalid_packages(clean_packages)
    return clean_packages


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


def _duplicate_package_warning(packages: list, packages_dev: list):
    seen = list_intersection(packages, packages_dev)

    for package in seen:
        _logger.warning(
            "\033[93mDuplicate package detected '%s'.\033[0m",
            package,
        )


def _remove_invalid_packages(packages: list[str]) -> list[str]:
    """Import the package and check if it contains a list of `django_apps`."""

    valid_packages = []

    for package in packages:
        try:
            module = importlib.import_module(package)
        except ModuleNotFoundError:
            _logger.warning(
                "\033[93mPackage '%s' could not be imported.\033[0m",
                package,
            )
            continue

        if not hasattr(module, "django_apps"):
            continue

        valid_packages.append(package)

    return valid_packages
