from functools import wraps

from channels.consumer import AsyncConsumer
from django import urls

from conreq import config
from conreq.utils.environment import get_base_url

BASE_URL = get_base_url(append_slash=False, prepend_slash=False)
if BASE_URL:
    BASE_URL = BASE_URL + "/"


def websocket(path: str, use_regex: bool = False) -> AsyncConsumer:
    """Decorates a websocket consumer class."""

    def decorator(class_: AsyncConsumer):

        websockets = config.asgi.websockets
        if not use_regex:
            websockets.append(urls.path(BASE_URL + path, class_.as_asgi()))
        else:
            websockets.append(urls.re_path(BASE_URL + path, class_.as_asgi()))

        @wraps(class_)
        def _wrapped_class(*args, **kwargs):
            return _wrapped_class(*args, **kwargs)

    return decorator


def asgi_middleware(
    dotted_path: str,
    positioning_element: str = None,
    positioning: str = "before",
) -> None:
    """Shortcut to add ASGI middleware to Django."""
    # TODO: Implement ASGI middleware
