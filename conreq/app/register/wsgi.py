from functools import wraps
from typing import Callable, Union

from django import urls
from django.views.generic import View

from conreq import app
from conreq.utils.environment import get_base_url

METRICS = None
BASE_URL = get_base_url(append_slash=False, prepend_slash=False)
if BASE_URL:
    BASE_URL = BASE_URL + "/"


def _load_performance_metrics():
    # pylint: disable=global-statement,import-outside-toplevel

    global METRICS

    if not METRICS:
        from conreq.utils.debug import performance_metrics

        METRICS = performance_metrics


def url(
    path: str,
    name: str = None,
    use_regex: bool = False,
) -> Union[Callable, View]:
    """Decorates a Django view function or view class."""

    def decorator(func_or_cls: Union[Callable, View]):

        _load_performance_metrics()

        if isinstance(func_or_cls, View):
            view = METRICS()(func_or_cls.as_view())
        else:
            view = METRICS()(func_or_cls)

        url_patterns = app.config.url_patterns
        if not use_regex:
            url_patterns.append(urls.path(BASE_URL + path, view, name=name))
        else:
            url_patterns.append(urls.re_path(BASE_URL + path, view, name=name))

        @wraps(view)
        def _wrapped_view(*args, **kwargs):
            return _wrapped_view(*args, **kwargs)

    return decorator


def api(
    path: str,
    version: int,
    use_regex: bool = False,
) -> View:
    """Decorates a DRF view function or view class."""

    def decorator(func_or_cls: Union[Callable, View]):

        _load_performance_metrics()

        if isinstance(func_or_cls, View):
            view = METRICS()(func_or_cls.as_view())
        else:
            view = METRICS()(func_or_cls)

        url_patterns = app.config.url_patterns
        if not use_regex:
            url_patterns.append(urls.path(f"{BASE_URL}/v{version}/{path}", view))
        else:
            url_patterns.append(urls.re_path(f"{BASE_URL}/v{version}/{path}", view))

        @wraps(view)
        def _wrapped_view(*args, **kwargs):
            return _wrapped_view(*args, **kwargs)

    return decorator
