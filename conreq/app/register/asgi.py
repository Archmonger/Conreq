from functools import wraps

from channels.consumer import AsyncConsumer
from django import urls

from conreq import app
from conreq.utils.environment import get_base_url

BASE_URL = get_base_url()


def websocket(path: str, use_regex: bool = False) -> AsyncConsumer:
    """Decorates a websocket consumer class."""

    def decorator(class_: AsyncConsumer):

        websockets = app.config("websockets")
        if not use_regex:
            websockets.append(urls.path(f"{BASE_URL}/{path}", class_.as_asgi()))
        else:
            websockets.append(urls.re_path(f"{BASE_URL}/{path}", class_.as_asgi()))

        @wraps(class_)
        def _wrapped_class(*args, **kwargs):
            return _wrapped_class(*args, **kwargs)

    return decorator
