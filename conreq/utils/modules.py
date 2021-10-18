import inspect
from importlib import import_module as _import
from types import ModuleType
from typing import Union


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
