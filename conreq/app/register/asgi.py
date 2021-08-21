from functools import wraps

from channels.consumer import AsyncConsumer

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable


def websocket(path: str, use_regex: bool = False) -> object:
    """Decorates a websocket consumer class."""

    def decorator(class_: AsyncConsumer):
        @wraps(class_)
        def _wrapped_class(*args, **kwargs):
            return _wrapped_class(*args, **kwargs)
