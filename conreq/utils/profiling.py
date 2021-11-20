"""Capabilities used while in DEBUG, that turn off in production environments."""

from conreq.utils.generic import DoNothingDecorator

# pylint: disable=invalid-name,too-few-public-methods,unused-import

metrics = DoNothingDecorator

# Set performance profiling capabilities depending on whether DEBUG=True
# TODO: Fix django silk periodically breaking
# if get_debug():
#     from silk.profiling.profiler import silk_profile as metrics
# else:
#     metrics = DoNothingDecorator
