from functools import wraps
from typing import Callable

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable


def user_setting(admin_only: bool = False) -> Callable:
    """Decorates an IDOM component. Component is injected into the user settings modal."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator
