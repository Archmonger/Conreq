import contextlib
from logging import getLogger
from pathlib import Path

import pkg_resources

from conreq.utils.environment import get_env

_logger = getLogger(__name__)


def find_packages(show_disabled: bool = False) -> list[str]:
    """Returns all available Conreq packages, typically installed from the app store."""
    installed_packages = get_env("INSTALLED_PACKAGES", [], return_type=list)
    if show_disabled:
        return installed_packages
    disabled_packages = get_env("DISABLED_PACKAGES", [], return_type=list)
    return [pkg for pkg in installed_packages if pkg not in disabled_packages]


def packages_to_modules(*packages: str) -> list[str]:
    """Returns all importable modules within the given packages."""

    modules = []

    for pkg in packages:
        # Parse eggs
        with contextlib.suppress(pkg_resources.DistributionNotFound, FileNotFoundError):
            import_names = _parse_top_level_txt(pkg)
            if import_names:
                modules.extend(import_names)
                continue

        # Parse wheel install records
        with contextlib.suppress(pkg_resources.DistributionNotFound, FileNotFoundError):
            import_names = _parse_records(pkg)
            if import_names:
                modules.extend(import_names)
                continue

        _logger.warning(
            "\033[93mCould not determine package info for '%s'. "
            "Package may misconfigured or not installed.\033[0m",
            pkg,
        )

    return modules


def _parse_top_level_txt(package: str) -> list[str]:
    """Returns all importable modules within the given package."""
    distribution = pkg_resources.get_distribution(package)
    return distribution.get_metadata("top_level.txt").splitlines()


def _parse_records(package: str) -> list[str]:
    distribution = pkg_resources.get_distribution(package)
    install_paths = distribution.get_metadata("RECORD").splitlines()
    names = set()
    for path in install_paths:
        path = path.split(",")[0]
        testable_path = Path(path)
        if len(testable_path.parts) <= 1:
            continue
        folder = testable_path.parts[0]
        if "." in folder:
            continue
        names.add(folder)
    return list(names)
