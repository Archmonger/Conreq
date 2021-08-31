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
