from inspect import iscoroutinefunction

from conreq import app
from conreq.utils.views import stub


async def landing(request):
    """Wrapper for the configurable landing view."""
    view = app.config.landing_view
    if view is landing:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request)
    return view(request)


async def home(request):
    """Wrapper for the configurable home view."""
    view = app.config.home_view
    if view is home:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request)
    return view(request)


async def sign_up(request):
    """Wrapper for the configurable sign up view."""
    view = app.config.sign_up_view
    if view is sign_up:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request)
    return view(request)


async def sign_in(request):
    """Wrapper for the configurable sign in view."""
    view = app.config.sign_in_view
    if view is sign_in:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request)
    return view(request)


async def password_reset(request):
    """Wrapper for the configurable password reset view."""
    view = app.config.password_reset_view
    if view is password_reset:
        return stub(request)
    if iscoroutinefunction(view):
        return await view(request)
    return view(request)
