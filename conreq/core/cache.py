"""Conreq Caching: Simplified caching module."""
from threading import Thread

from conreq.core import log
from conreq.core.generic_tools import clean_string
from conreq.core.thread_helper import ReturnThread
from django.core.cache import cache

# TODO: Obtain these values from the database on init
DEFAULT_CACHE_DURATION = 30 * 60  # Time in seconds

# Creating a logger (for log files)
__logger = log.get_logger("Caching")
log.configure(__logger, log.DEBUG)


def handler(
    cache_name,
    function=None,
    page_key="",
    force_update_cache=False,
    cache_duration=DEFAULT_CACHE_DURATION,
    **kwargs
):
    """Handles caching for results and data.

    Args:
        cache: Name of the cache to use.
        function: A function reference that returns some value to be cached. This function must only use **kwargs.
        page_key: The page name or page number to use as a key value.
        force_update_cache:
        cache_duration:
        **kwargs: Any parameters that need to be passed into "function".
    """

    cached_results = None
    # Looks through cache and will perform a search if needed.
    try:
        # If the function was actually a list, then use set_many and/or get_many
        # All items must belong to the same cache
        # { page_key: {
        #               "function": function_value,
        #               "kwargs": kwargs_value,
        #               "cache_key": cache_key_value, (optional)
        #             },
        # ... }
        if isinstance(function, dict):
            # Obtain all the keys from the passed in dictionary
            requested_keys = []
            for key, value in function.items():
                if value.__contains__("cache_key"):
                    cache_key = value["cache_key"]
                else:
                    cache_key = clean_string(
                        cache_name + "_kwargs" + str(kwargs) + "_key" + str(key)
                    )

                requested_keys.append(cache_key)

            # Search cache for all keys
            cached_results = cache.get_many(requested_keys)

            # If nothing was in cache, or cache was expired, run function()
            thread_list = []
            for cache_key in requested_keys:
                if not cached_results.__contains__(cache_key):
                    key = cache_key.split("_")[2][3:]
                    thread = ReturnThread(
                        target=function[key]["function"], kwargs=function[key]["kwargs"]
                    )
                    thread.start()
                    thread_list.append((cache_key, thread))

            missing_keys = {}
            for key, thread in thread_list:
                missing_keys[key] = thread.join()

            # Set values in cache for any newly executed functions
            if bool(missing_keys):
                Thread(
                    target=cache.set_many, args=[missing_keys, cache_duration]
                ).start()

            # Return all results
            cached_results.update(missing_keys)
            return cached_results

        # Get the cached value
        cache_key = clean_string(
            cache_name + "_kwargs" + str(kwargs) + "_key" + str(page_key)
        )
        cached_results = cache.get(cache_key)

        # No function was provided, just return bare cache value
        if function is None:
            return cached_results

        # If the user wants to force update the cache, nothing
        # was in cache, or cache was expired, run function()
        if cached_results is None or force_update_cache:
            function_results = function(**kwargs)
            cache.set(cache_key, function_results, cache_duration)
            return function_results

        # If a value was in cache and not expired, return that value
        if cached_results is not None:
            return cached_results

    except:
        # If the search threw an exception, return a cached value.
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
        if cached_results is None:
            return cache.get(cache_key)

        # No cached values to return. Exception must be handled elsewhere.
        raise
