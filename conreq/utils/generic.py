"""Generic functions to be used anywhere. All functions only have stdlib dependencies."""
import os
import pkgutil
from re import sub as substitution

ENV_PREFIX = os.environ.get("CONREQ_ENV_PREFIX", "").rstrip("_").upper()
if ENV_PREFIX:
    ENV_PREFIX = ENV_PREFIX + "_"


def is_key_value_in_list(key, value, search_list, return_item=False):
    """Iterate through a list of dicts to check if a specific key/value pair exists."""
    if isinstance(search_list, list):
        for item in search_list:
            if item.__contains__(key) and item[key] == value:
                if return_item:
                    return item
                return True

    # The key value pair could not be found in the list of dictionaries
    return False


def remove_duplicates_from_list(duplicate_list):
    """Returns a list that contains no duplicate values"""
    return list(dict.fromkeys(duplicate_list))


def clean_string(string):
    """Removes non-alphanumerics from a string"""
    try:
        return substitution(r"\W+", "", string).lower()
    except:
        return string


def get_base_url():
    """Obtains the base URL from the environment variables"""
    base_url = os.environ.get("BASE_URL", "")
    if isinstance(base_url, str) and base_url:
        base_url = base_url.replace("/", "").replace("\\", "")
        base_url = "/" + base_url
    return base_url


def str_to_bool(string, default_value=True):
    """Converts a string into a boolean."""
    if isinstance(string, str):
        if string.lower() == "true" or string == "1":
            return True
        if string.lower() == "false" or string == "0":
            return False
    return default_value


def get_bool_from_env(name, default_value=False):
    """Obtains a boolean from an environment variable"""
    env_var = os.environ.get(ENV_PREFIX + name)
    return str_to_bool(env_var, default_value)


def get_str_from_env(name, default_value=""):
    """Obtains a string from an environment variable"""
    return os.environ.get(ENV_PREFIX + name, default_value)


def get_int_from_env(name, default_value=0):
    """Obtains a integer from an environment variable"""
    env_var = os.environ.get(ENV_PREFIX + name)
    if env_var.isdigit():
        return int(env_var)
    return default_value


def get_env_prefix():
    """Returns the environment variables prefix that should be used."""
    return ENV_PREFIX


def get_debug_from_env():
    """Shortcut to obtain DEBUG from env variables"""
    return get_bool_from_env("DEBUG", True)


def get_database_type():
    """Determines what type of database the current Conreq instance should be using. Ex) MYSQL, SQLITE, etc."""
    db_engine = os.environ.get("DB_ENGINE", "")
    if db_engine.upper() == "MYSQL":
        return "MYSQL"
    return "SQLITE3"


def list_modules(path, prefix=""):
    """Returns all modules in a path"""
    return [name for _, name, _ in pkgutil.iter_modules([path], prefix=prefix)]


def list_modules_with(path, submodule_name, prefix=""):
    """Returns a tuple of all modules containing module name and an importable path to 'example.module.urls'"""
    modules = list_modules(path)
    module_files = []
    for module in modules:
        module_path = os.path.join(path, module)
        if submodule_name in list_modules(module_path):
            urls_path = prefix + module + "." + submodule_name
            module_files.append((module, urls_path))
    return module_files
