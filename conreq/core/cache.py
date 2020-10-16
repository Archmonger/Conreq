"""Conreq Caching: Simplified caching module."""
# Default Python Modules
from time import time

# TODO: Obtain these values from the database on init
MAX_CACHE_DURATION = 30 * 60  # Time in seconds


def handler(
    cache,
    cache_time,
    function,
    page_key=0,
    max_cache_duration=MAX_CACHE_DURATION,
    **kwargs
):
    """Handles caching for results and data.

    Args:
        cache:  Dictionary used for (Page name or page number, Results) pairs. Used for RAM caching.
        cache_time:  Dictionary used for (Page name or page number, Time Cached) pairs. Used for RAM caching.
        function: A function reference that returns something (ex. A function that obtains search results). This function must use **kwargs.
        page_key: The page name or page number to use as a key for the cache and cache_time dictionaries.
        **kwargs: Any additional parameters that need to be passed into "function".
    """
    # Looks through cache and will perform a search if needed
    if max_cache_duration is not None:
        # Search if this page has never been cached before
        if not cache.__contains__(page_key):
            cache[page_key] = function(**kwargs)
            cache_time[page_key] = time()

        # Search if the cache results are too old.
        elif time() - cache_time[page_key] > max_cache_duration:
            cache[page_key] = function(**kwargs)
            cache_time[page_key] = time()

        # Search if there are unreasonably few results in cache
        elif len(cache[page_key]) <= 1:
            cache[page_key] = function(**kwargs)
            cache_time[page_key] = time()

    # Return the values stored in cache
    return cache[page_key]
