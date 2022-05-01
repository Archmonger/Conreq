from functools import wraps
from typing import Callable, Union

import idom
from django.urls import path, re_path
from django_idom.hooks import use_websocket
from idom.core.types import ComponentType, VdomDict
from idom.html import div, iframe

from conreq import AuthLevel
from conreq.utils.environment import get_base_url
from conreq.utils.views import authenticated as authenticated_view

BASE_URL = get_base_url(prepend_slash=False, empty_if_unset=True)


def authenticated(
    fallback: Union[ComponentType, VdomDict] = None,
    auth_level: AuthLevel = AuthLevel.user,
) -> ComponentType:
    """Decorates an IDOM component."""

    def decorator(component):
        @wraps(component)
        def _wrapped_func(*args, **kwargs):
            websocket = use_websocket()

            if auth_level == AuthLevel.user:
                return (
                    component(*args, **kwargs)
                    if websocket.scope["user"].is_authenticated
                    else fallback or div()
                )

            if auth_level == AuthLevel.admin:
                return (
                    component(*args, **kwargs)
                    if websocket.scope["user"].is_staff
                    else fallback or div()
                )

            return component(*args, **kwargs)

        return _wrapped_func

    return decorator


# TODO: Use Django resolve and raise an exception if registering something that already exists
def view_to_component(
    url_pattern: str = None,
    name: str = None,
    use_regex: bool = False,
    auth_level: AuthLevel = AuthLevel.user,
) -> ComponentType:
    """Converts a Django view function/class into an IDOM component
    by turning it into an idom component in an iframe."""

    def decorator(func: Callable):
        # pylint: disable=import-outside-toplevel
        from conreq.urls import urlpatterns
        from conreq.utils.profiling import profiled_view

        # Register a new URL path
        view = profiled_view(authenticated_view(func, auth_level))
        dotted_path = f"{func.__module__}.{func.__name__}".replace("<", "").replace(
            ">", ""
        )
        view_name = name or dotted_path
        src_url = url_pattern or f"{BASE_URL}iframe/{dotted_path}"

        if use_regex:
            urlpatterns.append(re_path(src_url, view, name=view_name))
        else:
            urlpatterns.append(path(src_url, view, name=view_name))

        # Create an iframe with src=...
        @idom.component
        def idom_component(*args, **kwargs):
            return iframe({"src": f"/{src_url}", "loading": "lazy"})

        return idom_component

    return decorator
