from functools import wraps
from typing import Callable

from conreq import config


# TODO: Add the other tabs to here.
def user_setting(tab_name: str) -> Callable:
    """Decorates an IDOM component. Component is injected into the user settings modal.
    Settings component will be provided the websocket scope.
    """
    # TODO: Implement user settings tab registration

    def decorator(func):

        config.tabs.user_settings[tab_name] = {"component": func}

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator
