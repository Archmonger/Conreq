"""Conreq Caching: Simplified caching module."""
from conreq.utils import log
from conreq.utils.generic import (
    ReturnThread,
    clean_string,
    get_debug_from_env,
)
from django.core.cache import cache

if get_debug_from_env():
    print("Conreq is in DEBUG mode. Clearing cache...")
    cache.clear()

# Globals
DEFAULT_CACHE_DURATION = 60 * 60  # Time in seconds

# Creating a logger (for log files)
__logger = log.get_logger(__name__)


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


def __multi_execution(
    cache_name,
    function,
    cache_duration=DEFAULT_CACHE_DURATION,
):
    """Retrieve, set, and potentially execute multiple cache functions at once.
    Cached values obtained/set with django get_many/set_many cache API.
    Functions are executed using threading with a 5 second timeout.
    Functions must follow this format:
    {
      page_key : {
         "function": function_value,
         "kwargs": {kwargs_value},
         "args": [args_values],
      }, ...
    }"""
    requested_keys = []
    for key, value in function.items():
        cache_key = generate_cache_key(cache_name, value["args"], value["kwargs"], key)
        log.handler(
            cache_name + " - Multi-execution generated cache key " + cache_key,
            log.DEBUG,
            __logger,
        )
        requested_keys.append(cache_key)

    # Search cache for all keys
    cached_results = cache.get_many(requested_keys)
    log.handler(
        cache_name
        + " - Multi-execution detected "
        + str(len(cached_results))
        + " available keys.",
        log.INFO,
        __logger,
    )

    # If nothing was in cache, or cache was expired, run function()
    thread_list = []
    for cache_key in requested_keys:
        if not cached_results.__contains__(cache_key):
            key = obtain_key_from_cache_key(cache_key)
            thread = ReturnThread(
                target=function[key]["function"],
                args=function[key]["args"],
                kwargs=function[key]["kwargs"],
            )
            thread.start()
            thread_list.append((cache_key, thread))

    missing_keys = {}
    for key, thread in thread_list:
        missing_keys[key] = thread.join(timeout=5)

    # Set values in cache for any newly executed functions
    if bool(missing_keys):
        log.handler(
            cache_name
            + " - Multi-execution detected "
            + str(len(missing_keys))
            + " missing keys.",
            log.INFO,
            __logger,
        )
        cache.set_many(missing_keys, cache_duration)

    # Return all results
    cached_results.update(missing_keys)

    # If results were none, log it.
    if cached_results is None:
        log.handler(
            cache_name + " - Multi-execution generated no results!",
            log.WARNING,
            __logger,
        )

    return cached_results


def handler(
    cache_name,
    page_key="",
    function=None,
    force_update_cache=False,
    cache_duration=DEFAULT_CACHE_DURATION,
    args=(),
    kwargs=None,
):
    """Handles caching for results and data.

    Args:
        cache: Name of the cache to use.
        page_key: The page name or page number to use as a key value.
        function: The function to be executed if cached values are expired.
            If no function is provided, whatever was stored in cache is returned.
            If a dict was provided, get and save the values to cache using get_many and set_many. See __multi_execution() for more details.
        force_update_cache: Forces execution of function, regardless if values are expired or not.
        cache_duration: Duration in seconds that the cached value should be valid for.
        args: A list of arguements to pass into function.
        kwargs: A dictionary of keyworded arguements to pass into function.
    """

    cached_results = None
    if kwargs is None:
        kwargs = {}
    # Looks through cache and will perform a search if needed.
    try:
        log.handler(
            cache_name + " - Accessed.",
            log.DEBUG,
            __logger,
        )

        # If the function was actually a dict of functions, then retrieve values using multi-execution.
        if isinstance(function, dict):
            return __multi_execution(cache_name, function, cache_duration)

        # Get the cached value
        cache_key = generate_cache_key(cache_name, args, kwargs, page_key)
        cached_results = cache.get(cache_key)
        log.handler(
            cache_name + " - Generated cache key " + cache_key,
            log.DEBUG,
            __logger,
        )

        # No function was provided, just return a bare cache value
        if function is None:
            log.handler(
                cache_name + " - Requested raw cache values.",
                log.DEBUG,
                __logger,
            )
            return cached_results

        # If the user wants to force update the cache, nothing
        # was in cache, or cache was expired, run function()
        if cached_results is None or force_update_cache:
            function_results = function(*args, **kwargs)
            cache.set(cache_key, function_results, cache_duration)
            log.handler(
                cache_name + " - " + function.__name__ + "()",
                log.INFO,
                __logger,
            )
            return function_results

        if cached_results is None:
            log.handler(
                cache_name + " - Cache key " + cache_key + " was empty!",
                log.INFO,
                __logger,
            )

        # If a value was in cache and not expired, return that value
        return cached_results

    except:
        # If the function threw an exception, return none.
        if isinstance(function, dict):
            log.handler(
                "Function list failed to execute!",
                log.ERROR,
                __logger,
            )
        else:
            log.handler(
                "Function " + function.__name__ + " failed to execute!",
                log.ERROR,
                __logger,
            )
