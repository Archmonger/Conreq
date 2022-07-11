import inspect
import os
import pkgutil
from importlib import import_module as _import_module
from pathlib import Path
from types import ModuleType
from typing import Union


def import_module(
    dotted_path: str, *args, fail_silently: bool = False, **kwargs
) -> Union[ModuleType, None]:
    """
    Light wrapper for `importlib.import_module` that can fail silently.
    """
    try:
        return _import_module(dotted_path, *args, **kwargs)
    except ModuleNotFoundError as err:
        if not fail_silently:
            raise ImportError(f"{dotted_path} doesn't exist!") from err


def load(module: str, fail_silently: bool = False) -> ModuleType | None:
    """
    Imports a module relative to the caller's parent module and returns
    the module reference. Raise ImportError if the import failed.
    """
    # pylint: disable=unused-variable
    try:
        stack = inspect.stack()[1]
        full_module_path = inspect.getmodule(stack[0]).__name__
        parent_module, current_module = full_module_path.rsplit(".", 1)
        return import_module(".".join([parent_module, module]), fail_silently)
    except Exception as err:
        if not fail_silently:
            raise ImportError(f"{module} doesn't exist!") from err


def find_modules(folder_path: str | Path, prefix: str = "") -> list[str]:
    """Returns all modules in a path"""
    return [
        name for _, name, _ in pkgutil.iter_modules([str(folder_path)], prefix=prefix)
    ]


def find_modules_with(
    folder_path: str, submodule_name: str, prefix: str = ""
) -> list[str]:
    """Returns a tuple of all modules containing module name and an importable path to 'example.module.urls'"""
    modules = find_modules(folder_path)
    modules_with = []

    for module in modules:
        submodules = os.path.join(folder_path, module)
        if submodule_name in find_modules(submodules):
            modules_with.append(prefix + module)

    return modules_with
