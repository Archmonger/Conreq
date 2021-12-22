from functools import wraps
from typing import Any, Callable, Union

from django.urls import path, re_path
from django.views.generic import View

from conreq.utils.environment import get_base_url

# TODO: Use Django resolve and raise an exception if registering something that already exists
# pylint: disable=import-outside-toplevel

BASE_URL = get_base_url(append_slash=False, prepend_slash=False)
if BASE_URL:
    BASE_URL = BASE_URL + "/"


def url(
    url_pattern: str,
    name: str = None,
    use_regex: bool = False,
) -> Union[Callable, View]:
    """Decorates a Django view function or view class."""

    def decorator(new_path: Any):
        from conreq.urls import urlpatterns
        from conreq.utils.profiling import profiled_view

        view = profiled_view(new_path)

        if use_regex:
            urlpatterns.append(re_path(BASE_URL + url_pattern, view, name=name))
        else:
            urlpatterns.append(path(BASE_URL + url_pattern, view, name=name))

        @wraps(view)
        def _wrapped_view(*args, **kwargs):
            return _wrapped_view(*args, **kwargs)

    return decorator


def api(
    url_pattern: str,
    version: int,
    use_regex: bool = False,
) -> View:
    """Decorates a DRF view function or view class."""

    def decorator(new_path: Any):
        from conreq.urls import urlpatterns
        from conreq.utils.profiling import profiled_view

        view = profiled_view(new_path)

        if use_regex:
            urlpatterns.append(re_path(f"{BASE_URL}/v{version}/{url_pattern}", view))
        else:
            urlpatterns.append(path(f"{BASE_URL}/v{version}/{url_pattern}", view))

        @wraps(view)
        def _wrapped_view(*args, **kwargs):
            return _wrapped_view(*args, **kwargs)

    return decorator


def wsgi_middleware(
    dotted_path: str,
    positioning_element: str = None,
    positioning: str = "before",
) -> None:
    """Shortcut to add WSGI middleware to Django."""
    # TODO: Implement WSGI middleware
