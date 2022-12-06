"""Django caching wrapper and cache related capabilities."""

import logging
from collections.abc import Callable
from typing import Any, Sequence

from django.core.cache import cache as djcache
from huey.contrib.djhuey import db_task

from conreq.utils.generic import clean_string
from conreq.utils.threads import ReturnThread

DEFAULT_CACHE_DURATION = 3600  # Time in seconds
_logger = logging.getLogger(__name__)


def create_cache_key(cache_name: str, args: Sequence, kwargs: dict, key: str) -> str:
    """Generates a key to be used with django caching"""
    return clean_string(f"{cache_name}_args_{args}_kwargs_{kwargs}_key_{key}")


def obtain_key_from_cache_key(cache_key: str) -> str:
    """Parses the cache key and returns any values after the string '_key'"""
    return cache_key[cache_key.find("_key") + len("_key") :]


@db_task()
def _lazy_set_many(cache_dict, duration):
    """Sets a cache value through a background task"""
    djcache.set_many(cache_dict, duration)


@db_task()
def _lazy_set(cache_key, cache_value, duration):
    """Sets many cache values through a background task"""
    djcache.set(cache_key, cache_value, duration)


def get_or_set(
    cache_name: str,
    page_key: str = "",
    function: Callable | None = None,
    args: Sequence = (),
    kwargs: dict | None = None,
    duration: int = DEFAULT_CACHE_DURATION,
    force_update: bool = False,
) -> Any:
    """Handles caching for results and data. If the cached value is expired and a function is provided,
    the function is called and a new cached value will be set.

    Args:
        cache_name: Name prepended to cache get/set calls.
        page_key: A value to use as a page key.
        function: The function to be executed (if cached values are expired).
            If no function is provided, whatever was stored in cache is always returned.
        force_update: Forces execution of function, regardless if value is expired or not. Does not work with multi execution.
        duration: Duration in seconds that the cached value should be valid for.
        args: A list of arguements to pass into function.
        kwargs: A dictionary of keyworded arguements to pass into function.
    """

    cached_results = None
    if kwargs is None:
        kwargs = {}
    try:
        # Get the cached value
        _logger.debug("%s - Accessed.", cache_name)
        cache_key = create_cache_key(cache_name, args, kwargs, page_key)
        cached_results = djcache.get(cache_key)
        _logger.debug("%s - Generated cache key %s", cache_name, cache_key)

        # No function was provided, just return a bare cache value
        if function is None:
            _logger.debug("%s - Requested raw cache values.", cache_name)
            return cached_results

        # If the user wants to force update the cache, nothing
        # was in cache, or cache was expired, run function()
        if cached_results is None or force_update:
            function_results = function(*args, **kwargs)
            if function_results:
                _lazy_set(cache_key, function_results, duration)
            _logger.info("%s - %s()", cache_name, function.__name__)
            return function_results

        _logger.debug(
            "%s - Cache key %s contains %s!", cache_name, cache_key, str(cached_results)
        )

        # If a value was in cache and not expired, return that value
        return cached_results

    except Exception:
        _logger.exception(
            "Cache handler has failed to execute. Function: %s Cache Name: %s Page Key: %s",
            getattr(function, "__name__", function),
            cache_name,
            page_key,
        )
    return None


def get_or_set_many(
    cache_name: str,
    functions: dict[str, dict[str, Any]],
    duration: int = DEFAULT_CACHE_DURATION,
    timeout: int = 5,
) -> dict[str, Any] | None:
    """Retrieve, set, and potentially execute multiple cache functions at once.
    Functions must follow this format:

    {
      page_key : {
         "function": function_value,
         "args": [args_values],
         "kwargs": {kwargs_value},
      },
      ...
    }
    """
    try:
        _logger.debug("%s - Accessed.", cache_name)

        requested_keys = []
        for key, value in functions.items():
            cache_key = create_cache_key(
                cache_name, value["args"], value["kwargs"], key
            )
            _logger.debug(
                "%s - Cache multi execution generated cache key %s",
                cache_name,
                cache_key,
            )
            requested_keys.append(cache_key)

        # Search cache for all keys
        cached_results = djcache.get_many(requested_keys)
        _logger.info(
            "%s - Cache multi execution detected %d available keys.",
            cache_name,
            cached_results,
        )

        # If nothing was in cache, or cache was expired, run function()
        thread_list = []
        for cache_key in requested_keys:
            if cache_key in cached_results:
                key = obtain_key_from_cache_key(cache_key)
                thread = ReturnThread(
                    target=functions[key]["function"],
                    args=functions[key]["args"],
                    kwargs=functions[key]["kwargs"],
                )
                thread.start()
                thread_list.append((cache_key, thread))

        missing_keys = {
            key: thread.join(timeout=timeout) for key, thread in thread_list
        }

        # Set values in cache for any newly executed functions
        if bool(missing_keys):
            _logger.info(
                "%s - Cache multi execution detected %d missing keys.",
                cache_name,
                missing_keys,
            )
            _lazy_set_many(missing_keys, duration)

        # Return all results
        cached_results.update(missing_keys)

        # If results were none, log it.
        if cached_results is None:
            _logger.warning(
                "%s - Cache multi execution generated no results!", cache_name
            )

        return cached_results

    except Exception:
        _logger.exception("Functions %s failed to execute!", functions)
    return None
