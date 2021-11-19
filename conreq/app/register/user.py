from functools import wraps
from typing import Callable

import conreq


def user_setting() -> Callable:
    """Decorates an IDOM component. Component is injected into the user settings modal.
    Settings component will be provided the websocket scope.
    """

    def decorator(func):

        conreq.config.user_setting_sections.append(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator
