"""Performing profiling capabilities."""

from inspect import iscoroutinefunction
from typing import Any, Callable

from conreq.utils.environment import get_debug_mode
from conreq.utils.generic import DoNothingDecorator


def profiled_view(view: Any, name=None) -> Callable:
    """Helper utility to add performance profiling to a view class or function, if possible."""
    # Set view profiling capabilities depending on whether DEBUG=True
    if get_debug_mode():
        from silk.profiling.profiler import silk_profile as metrics
    else:
        metrics = DoNothingDecorator

    # Something that isn't a view function, such as a list of urlpatterns
    if not callable(view):
        return view

    # Async class or function views
    # FIXME: Currently not supported by django-silk
    if iscoroutinefunction(view) or getattr(view, "view_is_async", False):
        return view

    # Sync class view
    dotted_path = f"{view.__module__}.{view.__name__}"
    if hasattr(view, "as_view"):
        view.dispatch = metrics(name=name or dotted_path)(view.dispatch)
        return view.as_view()

    # Sync function view
    return metrics(name=name or dotted_path)(view)
