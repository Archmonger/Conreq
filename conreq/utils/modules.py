import inspect
from importlib import import_module


def load_module(dotted_path: str, fail_silently: bool = False):
    """
    Import a dotted module path and return the module reference.
    Raise ImportError if the import failed.
    """
    try:
        return import_module(dotted_path)
    except ModuleNotFoundError as err:
        if not fail_silently:
            raise ImportError(f"{dotted_path} doesn't exist!") from err


def load(module: str, fail_silently: bool = False):
    """
    Imports a module relative to the caller's parent module and returns
    the module reference. Raise ImportError if the import failed.
    """
    # pylint: disable=unused-variable
    stack = inspect.stack()[1]
    full_module_path = inspect.getmodule(stack[0]).__name__
    parent_module, current_module = full_module_path.rsplit(".", 1)
    return load_module(".".join([parent_module, module]), fail_silently)
