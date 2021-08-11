"""Generic functions to be used anywhere. All functions only have stdlib dependencies."""
import os
import pkgutil
from re import sub


def is_key_value_in_list(
    key: any, value: any, search_list: list, return_item: bool = False
):
    """Iterate through a list of dicts to check if a specific key/value pair exists."""
    if isinstance(search_list, list):
        for item in search_list:
            if item.__contains__(key) and item[key] == value:
                if return_item:
                    return item
                return True
    return False


def remove_duplicates_from_list(duplicate_list: list):
    """Returns a list that contains no duplicate values"""
    return list(dict.fromkeys(duplicate_list))


def clean_string(string: str):
    """Removes non-alphanumerics from a string"""
    return sub(r"\W+", "", string).lower()


def str_to_bool(string: str, default_value: bool = True):
    """Converts a string into a boolean."""
    if isinstance(string, str):
        if string.lower() == "true" or string == "1":
            return True
        if string.lower() == "false" or string == "0":
            return False
    return default_value


def list_modules(path: str, prefix: str = ""):
    """Returns all modules in a path"""
    return [name for _, name, _ in pkgutil.iter_modules([path], prefix=prefix)]


def list_modules_with(path: str, submodule_name: str, prefix: str = ""):
    """Returns a tuple of all modules containing module name and an importable path to 'example.module.urls'"""
    modules = list_modules(path)
    module_files = []
    for module in modules:
        module_path = os.path.join(path, module)
        if submodule_name in list_modules(module_path):
            urls_path = prefix + module + "." + submodule_name
            module_files.append((module, urls_path))
    return module_files
