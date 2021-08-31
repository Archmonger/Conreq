"""Capabilities used while in DEBUG, that turn off in production environments."""
from conreq.utils.environment import get_debug


# pylint: disable=invalid-name,too-few-public-methods,unused-import


class DoNothing:
    """Decorator that does nothing"""

    def __call__(self, target):
        return target


# Set performance profiling capabilities depending on whether DEBUG=True
if get_debug():
    from silk.profiling.profiler import silk_profile as metrics

else:
    metrics = DoNothing
