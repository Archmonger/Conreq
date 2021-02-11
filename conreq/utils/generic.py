import os
from re import sub as substitution
from threading import Thread


class ReturnThread(Thread):
    """Wrapper for python threads, however, these return a value."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None  # child class's variable, not available in parent.

    def run(self):
        """
        The original run method does not return value after self._target is run.
        This child class added a return value.
        :return:
        """
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args, **kwargs):
        """
        Join normally like the parent class, but added a return value which
        the parent class join method does not have.
        """
        super().join(*args, **kwargs)
        return self._return


def threaded_execution(function_list, args_list):
    """Threaded execution of function calls. All functions utilize the same args.
    Args:
        function_list: List containing references to functions
        args_list: List containing the arguments to be used for these function calls
    """
    thread_list = []
    results = []

    for function in function_list:
        thread = ReturnThread(
            target=function,
            args=args_list,
        )
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        results.append(thread.join())

    return results


def threaded_execution_unique_args(functions):
    """Executes functions with unique arguements. It will return all returned values as a list.
    To use this, pass in a list of dicts in the following format
        [{
            "function": foobar,
            "args": [],
            "kwargs": {},
            }, ...
        ]
    """

    # Begin a thread for each function
    thread_list = []
    for executable in functions:
        thread = ReturnThread(
            target=executable["function"],
            args=executable.get("args", None),
            kwargs=executable.get("kwargs", None),
        )
        thread.start()
        thread_list.append(thread)

    # Combine the results into one list
    results = []
    for index, thread in enumerate(thread_list):
        result = None
        try:
            result = thread.join()
        except:
            pass
        results.insert(index, result)

    return results


def generate_cache_key(cache_name, cache_args, cache_kwargs, key):
    """Generates a key to be used with django caching"""
    return clean_string(
        cache_name
        + "_args"
        + str(cache_args)
        + "_kwargs"
        + str(cache_kwargs)
        + "_key"
        + str(key)
    )


def obtain_key_from_cache_key(cache_key):
    """Parses the cache key and returns any values after the string '_key'"""
    return cache_key[cache_key.find("_key") + len("_key") :]


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


def get_bool_from_env(name, default_value):
    """Obtains a boolean from an environment variable"""
    env_var = os.environ.get(name)
    if isinstance(env_var, str):
        if env_var.lower() == "true":
            return True
        if env_var.lower() == "false":
            return False
    return default_value


def get_debug_from_env():
    """Shortcut to obtain DEBUG from env variables"""
    return get_bool_from_env("DEBUG", True)