import inspect
import pkgutil
from importlib import import_module as _import
from types import ModuleType
from typing import Union

from django.apps import AppConfig

SKIP_MODULE_NAMES = {
    "admin",
    "apps",
    "migrations",
    "templatetags",
    "management",
}


def import_module(
    dotted_path: str, *args, fail_silently: bool = False, **kwargs
) -> Union[ModuleType, None]:
    """
    Light wrapper for `importlib.import_module` that can fail silently.
    """
    try:
        return _import(dotted_path, *args, **kwargs)
    except ModuleNotFoundError as err:
        if not fail_silently:
            raise ImportError(f"{dotted_path} doesn't exist!") from err
        return None


def load(module: str, fail_silently: bool = False):
    """
    Imports a module relative to the caller's parent module and returns
    the module reference. Raise ImportError if the import failed.
    """
    # pylint: disable=unused-variable
    stack = inspect.stack()[1]
    full_module_path = inspect.getmodule(stack[0]).__name__
    parent_module, current_module = full_module_path.rsplit(".", 1)
    return import_module(".".join([parent_module, module]), fail_silently)


def autoload_modules(app_config: AppConfig):
    """Autoloads modules when the AppConfig registry is fully populated."""
    if not getattr(app_config, "autoload_modules", False):
        return

    fail_silently = getattr(app_config, "autoload_fail_silently", False)

    for loader, module_name, is_pkg in pkgutil.walk_packages([app_config.path]):
        try:
            if module_name not in SKIP_MODULE_NAMES:
                _import(".".join([app_config.name, module_name]))
                if is_pkg:
                    loader.find_module(module_name).load_module(module_name)
        except Exception as exception:
            if not fail_silently:
                raise exception
