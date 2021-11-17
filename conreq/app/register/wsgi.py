from functools import wraps
from inspect import isclass
from typing import Any, Callable, Union

from django.urls import path, re_path
from django.views.generic import View

from conreq.utils.environment import get_base_url

# pylint: disable=import-outside-toplevel

BASE_URL = get_base_url(append_slash=False, prepend_slash=False)
if BASE_URL:
    BASE_URL = BASE_URL + "/"


def url(
    pattern: str,
    name: str = None,
    use_regex: bool = False,
) -> Union[Callable, View]:
    """Decorates a Django view function or view class."""
    from conreq.urls import urlpatterns

    # TODO: Split URLs at every slash and create nested URLpatterns for every registered URL.
    # Would improve performance of the Django URL router significantly for configurations
    # with large numbers of registered URLs.

    def decorator(new_path: Any):

        from conreq.utils.profiling import metrics

        if not callable(new_path):
            view = new_path
        elif isclass(new_path):
            view = metrics()(new_path.as_view())
        else:
            view = metrics()(new_path)

        if not use_regex:
            urlpatterns.append(path(BASE_URL + pattern, view, name=name))
        else:
            urlpatterns.append(re_path(BASE_URL + pattern, view, name=name))

        @wraps(view)
        def _wrapped_view(*args, **kwargs):
            return _wrapped_view(*args, **kwargs)

    return decorator


def api(
    pattern: str,
    version: int,
    use_regex: bool = False,
) -> View:
    """Decorates a DRF view function or view class."""
    from conreq.urls import urlpatterns

    def decorator(new_path: Any):

        from conreq.utils.profiling import metrics

        if not callable(new_path):
            view = new_path
        elif isclass(new_path):
            view = metrics()(new_path.as_view())
        else:
            view = metrics()(new_path)

        if not use_regex:
            urlpatterns.append(path(f"{BASE_URL}/v{version}/{pattern}", view))
        else:
            urlpatterns.append(re_path(f"{BASE_URL}/v{version}/{pattern}", view))

        @wraps(view)
        def _wrapped_view(*args, **kwargs):
            return _wrapped_view(*args, **kwargs)

    return decorator


def middleware(
    dotted_path: str,
    positioning_element: str = None,
    positioning: str = "before",
) -> None:
    """Shortcut to add middleware to Django."""
    # TODO: Implement this
