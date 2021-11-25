from inspect import iscoroutinefunction

from channels.db import database_sync_to_async as convert_to_async

import conreq
from conreq.utils.views import stub


async def landing(request, *args, **kwargs):
    """Wrapper for the configurable landing view."""
    view = conreq.config.landing_view
    if view is landing:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def home(request, *args, **kwargs):
    """Wrapper for the configurable home view."""
    view = conreq.config.home_view
    if view is home:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def sign_up(request, *args, **kwargs):
    """Wrapper for the configurable sign up view."""
    view = conreq.config.sign_up_view
    if view is sign_up:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def sign_in(request, *args, **kwargs):
    """Wrapper for the configurable sign in view."""
    view = conreq.config.sign_in_view
    if view is sign_in:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def password_reset(request, *args, **kwargs):
    """Wrapper for the configurable password reset view."""
    view = conreq.config.password_reset_view
    if view is password_reset:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def password_reset_sent(request, *args, **kwargs):
    """Wrapper for the configurable password reset view."""
    view = conreq.config.password_reset_sent_view
    if view is password_reset:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)
