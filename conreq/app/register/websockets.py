from channels.consumer import AsyncConsumer
from django import urls

from conreq import config
from conreq.utils.environment import get_base_url

BASE_URL = get_base_url(prepend_slash=False, empty_if_unset=True)


def websocket(path: str, use_regex: bool = False):
    """Decorates a websocket consumer class."""

    def decorator(consumer: AsyncConsumer):
        websockets = config.asgi.websockets
        if not use_regex:
            websockets.append(urls.path(BASE_URL + path, consumer.as_asgi()))  # type: ignore
        else:
            websockets.append(urls.re_path(BASE_URL + path, consumer.as_asgi()))  # type: ignore
        return consumer

    return decorator
