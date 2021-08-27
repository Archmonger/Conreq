from functools import wraps
from typing import Callable, Union

from django import urls
from django.views.generic import View

from conreq import app
from conreq.utils.environment import get_base_url

BASE_URL = get_base_url(append_slash=False, prepend_slash=False)
if BASE_URL:
    BASE_URL = BASE_URL + "/"


def url(
    path: str,
    name: str = None,
    use_regex: bool = False,
) -> Union[Callable, View]:
    """Decorates a Django view function or view class."""

    def decorator(func_or_cls: Union[Callable, View]):

        view = func_or_cls
        if isinstance(func_or_cls, View):
            view = view.as_view()

        url_patterns = app.config("url_patterns")
        if not use_regex:
            url_patterns.append(urls.path(BASE_URL + path, func_or_cls, name=name))
        else:
            url_patterns.append(urls.re_path(BASE_URL + path, func_or_cls, name=name))

        @wraps(func_or_cls)
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

        view = func_or_cls
        if isinstance(func_or_cls, View):
            view = view.as_view()

        url_patterns = app.config("url_patterns")
        if not use_regex:
            url_patterns.append(urls.path(f"{BASE_URL}/v{version}/{path}", func_or_cls))
        else:
            url_patterns.append(
                urls.re_path(f"{BASE_URL}/v{version}/{path}", func_or_cls)
            )

        @wraps(func_or_cls)
        def _wrapped_view(*args, **kwargs):
            return _wrapped_view(*args, **kwargs)

    return decorator
