from functools import wraps
from typing import Callable

from django.urls import path
from django.urls.base import reverse
from idom.core.proto import VdomDict
from idom.core.vdom import make_vdom_constructor
from idom.html import div

from conreq.utils.environment import get_base_url

BASE_URL = get_base_url(append_slash=False, prepend_slash=False)
if BASE_URL:
    BASE_URL = BASE_URL + "/"
iframe = make_vdom_constructor("iframe")


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


def django_to_idom(func: Callable) -> VdomDict:
    """Converts a Django view function/class into an IDOM component."""
    # pylint: disable=import-outside-toplevel
    from conreq.urls import urlpatterns
    from conreq.utils.profiling import profiled_view

    # Add a /viewport/path.to.component URL
    view = profiled_view(func)
    view_name = func.__qualname__
    urlpatterns.append(path(BASE_URL + view_name, view))

    # Create an iframe with src=/viewport/path.to.component
    return iframe({"src": reverse(view_name)})
