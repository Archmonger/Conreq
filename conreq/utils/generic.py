"""Generic functions to be used anywhere. All functions only have stdlib dependencies."""
import os
from re import sub as substitution


def is_key_value_in_list(key, value, search_list, return_item=False):
    """Iterate through each result and check for the key/value pair"""
    for item in search_list:
        if item.__contains__(key) and item[key] == value:
            if return_item:
                return item
            return True

    # The key value pair could not be found in the list of dictionaries
    return False


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
        base_url = base_url.replace("/", "")
        base_url = base_url + "/"
    return base_url


def str_to_bool(string, default_value=True):
    if isinstance(string, str):
        if string.lower() == "true":
            return True
        if string.lower() == "false":
            return False
    return default_value


def get_bool_from_env(name, default_value):
    """Obtains a boolean from an environment variable"""
    env_var = os.environ.get(name)
    return str_to_bool(env_var, default_value)


def get_debug_from_env():
    """Shortcut to obtain DEBUG from env variables"""
    return get_bool_from_env("DEBUG", True)
