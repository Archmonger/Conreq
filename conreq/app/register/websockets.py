from channels.consumer import AsyncConsumer
from django import urls

from conreq import config
from conreq.utils.environment import get_base_url

BASE_URL = get_base_url(prepend_slash=False, empty_if_unset=True)


def websocket(path: str, use_regex: bool = False) -> AsyncConsumer:
    """Decorates a websocket consumer class."""

    def decorator(class_: AsyncConsumer):

        websockets = config.asgi.websockets
        if not use_regex:
            websockets.append(urls.path(BASE_URL + path, class_.as_asgi()))
        else:
            websockets.append(urls.re_path(BASE_URL + path, class_.as_asgi()))

        return class_

    return decorator


def middleware(
    dotted_path: str,
    positioning_elements: list[str] = None,
    positioning: str = "before",
    reverse: bool = False,
) -> None:
    """Shortcut to add ASGI middleware to Django."""
    # TODO: Implement ASGI middleware