from inspect import iscoroutinefunction

from channels.db import database_sync_to_async as convert_to_async

from conreq import config
from conreq.utils.views import stub

# TODO: Add warnings for sync code


async def landing(request, *args, **kwargs):
    """Configurable landing view."""
    view = config.views.landing
    if view is landing:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def home(request, *args, **kwargs):
    """Configurable home view."""
    view = config.views.home
    if view is home:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def sign_up(request, *args, **kwargs):
    """Configurable sign up view."""
    view = config.views.sign_up
    if view is sign_up:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def sign_in(request, *args, **kwargs):
    """Configurable sign in view."""
    view = config.views.sign_in
    if view is sign_in:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def password_reset(request, *args, **kwargs):
    """Configurable password reset view."""
    view = config.views.password_reset
    if view is password_reset:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def password_reset_sent(request, *args, **kwargs):
    """Configurable password reset sent view."""
    view = config.views.password_reset_sent
    if view is password_reset_sent:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def password_reset_confirm(request, *args, **kwargs):
    """Configurable password reset confirmation view."""
    view = config.views.password_reset_confirm
    if view is password_reset_confirm:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def offline(request, *args, **kwargs):
    """Configurable password reset confirmation view."""
    view = config.views.offline
    if view is offline:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)
