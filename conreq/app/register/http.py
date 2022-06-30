from functools import wraps
from typing import Any, Callable, Union

from django.urls import path, re_path
from django.views.generic import View

# TODO: Use Django resolve and raise an exception if registering something that already exists
# pylint: disable=import-outside-toplevel


def url(
    url_pattern: str,
    name: str = None,
    use_regex: bool = False,
) -> Union[Callable, View]:
    """Decorates a Django view function or view class."""

    def decorator(new_path: Any):
        from conreq.urls import conreq_urls
        from conreq.utils.profiling import profiled_view

        view = profiled_view(new_path)

        if use_regex:
            conreq_urls.append(re_path(url_pattern, view, name=name))
        else:
            conreq_urls.append(path(url_pattern, view, name=name))

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
        from conreq.urls import conreq_urls
        from conreq.utils.profiling import profiled_view

        view = profiled_view(new_path)

        if use_regex:
            conreq_urls.append(re_path(f"v{version}/{url_pattern}", view))
        else:
            conreq_urls.append(path(f"v{version}/{url_pattern}", view))

        return view

    return decorator


def middleware(
    dotted_path: str,
    positioning_elements: list[str] = None,
    positioning: str = "before",
    reverse: bool = False,
) -> None:
    """Shortcut to add WSGI middleware to Django."""
    # TODO: Implement WSGI middleware
