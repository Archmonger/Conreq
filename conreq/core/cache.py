"""Conreq Caching: Simplified caching module."""
from conreq.core import log
from conreq.core.generic_tools import clean_string
from conreq.core.thread_helper import ReturnThread
from django.core.cache import cache

# TODO: Obtain these values from the database on init
DEFAULT_CACHE_DURATION = 60 * 60  # Time in seconds

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
        log.handler(
            "Accessed cache " + cache_name,
            log.DEBUG,
            __logger,
        )

        # If the function was actually a list, then use set_many and/or get_many
        # All items must belong to the same cache
        # { page_key: {
        #               "function": function_value,
        #               "kwargs": {kwargs_value},
        #               "args": [args_values],
        #             },
        # ... }
        if isinstance(function, dict):
            if len(function) == 0:
                # Nothing was passed in
                return None
            else:
                # Obtain all the keys from the passed in dictionary
                requested_keys = []
                for key, value in function.items():
                    cache_key = clean_string(
                        cache_name + "_kwargs" + str(kwargs) + "_key" + str(key)
                    )
                    log.handler(
                        cache_name
                        + " multi-execution generated cache key "
                        + cache_key,
                        log.DEBUG,
                        __logger,
                    )
                    requested_keys.append(cache_key)

                # Search cache for all keys
                cached_results = cache.get_many(requested_keys)
                log.handler(
                    cache_name
                    + " multi-execution available keys: "
                    + str(len(cache_key)),
                    log.DEBUG,
                    __logger,
                )

                # If nothing was in cache, or cache was expired, run function()
                thread_list = []
                for cache_key in requested_keys:
                    if not cached_results.__contains__(cache_key):
                        key = cache_key.split("_")[2][3:]
                        thread = ReturnThread(
                            target=function[key]["function"],
                            args=function[key]["args"],
                            kwargs=function[key]["kwargs"],
                        )
                        thread.start()
                        thread_list.append((cache_key, thread))

                missing_keys = {}
                for key, thread in thread_list:
                    missing_keys[key] = thread.join()

                # Set values in cache for any newly executed functions
                if bool(missing_keys):
                    log.handler(
                        cache_name
                        + " multi-execution missing keys: "
                        + str(len(missing_keys)),
                        log.DEBUG,
                        __logger,
                    )
                    cache.set_many(missing_keys, cache_duration)

                # Return all results
                cached_results.update(missing_keys)

                # If results were none, log it.
                if cached_results is None:
                    log.handler(
                        cache_name + " multi-execution had no results!",
                        log.WARNING,
                        __logger,
                    )

                return cached_results

        # Get the cached value
        cache_key = clean_string(
            cache_name + "_kwargs" + str(kwargs) + "_key" + str(page_key)
        )
        log.handler(
            cache_name + " generated cache key " + cache_key,
            log.DEBUG,
            __logger,
        )
        cached_results = cache.get(cache_key)

        # No function was provided, just return bare cache value
        if function is None:
            log.handler(
                cache_name + " requested raw cache values.",
                log.DEBUG,
                __logger,
            )
            return cached_results

        # If the user wants to force update the cache, nothing
        # was in cache, or cache was expired, run function()
        if cached_results is None or force_update_cache:
            function_results = function(**kwargs)
            log.handler(
                cache_name + " function " + function.__name__ + " executed!",
                log.INFO,
                __logger,
            )
            cache.set(cache_key, function_results, cache_duration)
            return function_results

        if cached_results is None:
            log.handler(
                cache_name + " is not in the cache handler!",
                log.INFO,
                __logger,
            )

        # If a value was in cache and not expired, return that value
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

        return cache.get(cache_key)
