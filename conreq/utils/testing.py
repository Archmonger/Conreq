from channels.db import database_sync_to_async
from conreq.utils.generic import get_debug_from_env


def do_nothing(function=None):
    return function


# Disable async view rendering in debug to allow for performance profiling
if get_debug_from_env():
    convert_to_async = do_nothing
else:
    convert_to_async = database_sync_to_async
