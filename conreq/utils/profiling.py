"""Capabilities used while in DEBUG, that turn off in production environments."""

from inspect import isclass, iscoroutinefunction
from typing import Any

from conreq.utils.environment import get_debug
from conreq.utils.generic import DoNothingDecorator

# pylint: disable=invalid-name,too-few-public-methods,unused-import

metrics = DoNothingDecorator

# Set performance profiling capabilities depending on whether DEBUG=True

if get_debug():
    from silk.profiling.profiler import silk_profile as metrics
else:
    metrics = DoNothingDecorator


def profiled_view(view: Any, name=None, as_view=True):
    """Helper utility to add performance profiling to a view class or function, if possible."""
    # Something that isn't a view function, such as a list of urlpatterns
    if not callable(view):
        return view

    # Class view
    dotted_path = f"{view.__module__}.{view.__qualname__}"
    if isclass(view):
        view.dispatch = metrics(name=name or dotted_path)(view.dispatch)
        return view.as_view() if as_view else view

    # FIXME: Async views currently not supported by django-silk
    if iscoroutinefunction(view):
        return view

    # Function view
    return metrics(name=name or dotted_path)(view)
