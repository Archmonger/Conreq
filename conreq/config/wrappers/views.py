from inspect import iscoroutinefunction

from channels.db import database_sync_to_async as convert_to_async

from conreq import config

# pylint: disable=import-outside-toplevel
# TODO: All these views will eventually need to be made async, after more broad Django asyc support.
# Specifically, Django support for async decorators, template rendering, and ORM queries.


async def landing(request, *args, **kwargs):
    """Configurable landing view."""
    view = config.views.landing
    if view is None:
        from conreq._core.landing import views

        return await convert_to_async(views.landing)(request, *args, **kwargs)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def home(request, *args, **kwargs):
    """Configurable home view."""
    view = config.views.home
    if view is None:
        from conreq._core.home import views

        return await convert_to_async(views.home)(request, *args, **kwargs)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def sign_up(request, *args, **kwargs):
    """Configurable sign up view."""
    view = config.views.sign_up
    if view is None:
        from conreq._core.sign_up import views

        return await convert_to_async(views.sign_up)(request, *args, **kwargs)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def sign_in(request, *args, **kwargs):
    """Configurable sign in view."""
    view = config.views.sign_in
    if view is None:
        from conreq._core.sign_in import views

        return await convert_to_async(views.sign_in)(request, *args, **kwargs)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def password_reset(request, *args, **kwargs):
    """Configurable password reset view."""
    view = config.views.password_reset
    if view is None:
        from conreq._core.password_reset import views

        return await convert_to_async(views.PasswordResetView.as_view())(
            request, *args, **kwargs
        )
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def password_reset_sent(request, *args, **kwargs):
    """Configurable password reset sent view."""
    view = config.views.password_reset_sent
    if view is None:
        from conreq._core.password_reset import views

        return await convert_to_async(views.PassWordResetSentView.as_view())(
            request, *args, **kwargs
        )
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def password_reset_confirm(request, *args, **kwargs):
    """Configurable password reset confirmation view."""
    view = config.views.password_reset_confirm
    if view is None:
        from conreq._core.password_reset import views

        return await convert_to_async(views.PasswordResetConfirmView.as_view())(
            request, *args, **kwargs
        )
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def offline(request, *args, **kwargs):
    """Configurable offline view."""
    view = config.views.offline
    if view is None:
        from conreq._core.pwa import views

        return await convert_to_async(views.offline)(request, *args, **kwargs)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def service_worker(request, *args, **kwargs):
    """Configurable service worker view."""
    view = config.views.service_worker
    if view is None:
        from conreq._core.pwa import views

        return await convert_to_async(views.service_worker)(request, *args, **kwargs)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)


async def web_manifest(request, *args, **kwargs):
    """Configurable web manifest view."""
    view = config.views.web_manifest
    if view is None:
        from conreq._core.pwa import views

        return await convert_to_async(views.web_manifest)(request, *args, **kwargs)
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    return await convert_to_async(view)(request, *args, **kwargs)
