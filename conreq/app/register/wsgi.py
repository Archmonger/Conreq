from functools import wraps

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable


def url(path: str, use_regex: bool = False) -> object:
    """Decorates a Django view function."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def api(path: str, version: int, auth: bool = True, use_regex: bool = False) -> object:
    """Decorates a DRF view function."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)
