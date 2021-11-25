"""Capabilities used while in DEBUG, that turn off in production environments."""

from inspect import isclass
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


def profiled_view(view: Any):
    """Helper utility to add performance profiling to a view class or function, if possible."""

    if not callable(view):
        return view
    elif isclass(view):
        return metrics()(view.as_view())
    return metrics()(view)
