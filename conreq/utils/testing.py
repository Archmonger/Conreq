from functools import wraps

from conreq.utils.generic import get_debug_from_env


def do_nothing(function=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator(function)


class DoNothing(object):
    def __call__(self, target):
        return target


# Disable async view rendering in debug to allow for performance profiling
if get_debug_from_env():
    from silk.profiling.profiler import silk_profile

    class performance_metrics(silk_profile):
        pass


else:

    class performance_metrics(DoNothing):
        pass
