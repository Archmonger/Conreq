from functools import wraps
from typing import Callable

from idom.html import div


def authenticated(
    fallback: str = None,
) -> Callable:
    """Decorates an IDOM component."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(websocket, *args, **kwargs):
            return (
                func(websocket, *args, **kwargs)
                if websocket.scope["user"].is_authenticated
                else fallback or div()
            )

        return _wrapped_func

    return decorator
