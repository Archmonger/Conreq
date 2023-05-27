import importlib
import inspect
import os
import pkgutil
from importlib import import_module as _import_module
from logging import getLogger
from pathlib import Path
from types import ModuleType

_logger = getLogger(__name__)


def import_module(
    dotted_path: str, *args, fail_silently: bool = False, **kwargs
) -> ModuleType | None:
    """
    Light wrapper for `importlib.import_module` that can fail silently.
    """
    try:
        return _import_module(dotted_path, *args, **kwargs)
    except ModuleNotFoundError as err:
        if not fail_silently:
            raise ImportError(f"{dotted_path} doesn't exist!") from err

    return None


def load(module: str, fail_silently: bool = False) -> ModuleType | None:
    """
    Imports a module relative to the caller's parent module and returns
    the module reference. Raise ImportError if the import failed.
    """
    # pylint: disable=unused-variable
    try:
        stack = inspect.stack()[1]
        full_module_path = getattr(inspect.getmodule(stack[0]), "__name__")
        parent_module, current_module = full_module_path.rsplit(".", 1)
        return import_module(".".join([parent_module, module]), fail_silently)
    except Exception as err:
        if not fail_silently:
            raise ImportError(f"{module} doesn't exist!") from err

    return None


def find_modules(folder_path: str | Path, prefix: str = "") -> list[str]:
    """Returns all modules in a path"""
    return [
        name for _, name, _ in pkgutil.iter_modules([str(folder_path)], prefix=prefix)
    ]


def find_modules_with(
    folder_path: str, submodule_name: str, prefix: str = ""
) -> list[str]:
    """Returns a list of modules containing a submodule with the given name."""
    modules = find_modules(folder_path)
    modules_with = []

    for module in modules:
        submodules = os.path.join(folder_path, module)
        if submodule_name in find_modules(submodules):
            modules_with.append(prefix + module)

    return modules_with


def find_wildcards(dotted_path: str) -> set[str]:
    """Returns all dotted paths of all modules within a given wildcard directory.
    This is currently limited to trailing wildcards."""
    # TODO: Support non-trailing wildcards

    if not dotted_path.endswith(".*"):
        raise ValueError(f"App '{dotted_path}' does not end with '.*'.")

    dotted_path = dotted_path[:-2]
    apps_container = import_module(dotted_path)
    if not apps_container:
        _logger.warning(
            "\033[93mApp '%s' could not be imported.\033[0m",
            dotted_path,
        )
        return set()

    module_names = find_modules(apps_container.__path__[0])
    return {f"{dotted_path}.{name}" for name in module_names}


def validate_conreq_modules(module_names: list[str]) -> list[str]:
    """Check if modules are properly configured for Conreq.
    Returns a new list of valid modules."""

    valid_packages = []

    for package in module_names:
        try:
            module = importlib.import_module(package)
        except ModuleNotFoundError:
            _logger.warning(
                "\033[93mPackage '%s' could not be imported.\033[0m",
                package,
            )
            continue
        except Exception:
            _logger.exception(
                "\033[93mAn unknown error has occurred while importing '%s'.\033[0m",
                package,
            )
            continue

        if not hasattr(module, "conreq_apps"):
            _logger.warning(
                "\033[93mPackage '%s' is not properly configured. "
                "Please define `conreq_apps`.\033[0m",
                package,
            )
            continue

        valid_packages.append(package)

    return valid_packages
