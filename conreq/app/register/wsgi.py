from functools import wraps
from typing import Callable

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable


def url(path: str, name: str = None, use_regex: bool = False) -> Callable:
    """Decorates a Django view function."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator


def api(
    path: str,
    version: int,
    auth: bool = True,
    use_regex: bool = False,
) -> Callable:
    """Decorates a DRF view function."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator
