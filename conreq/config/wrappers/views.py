from inspect import iscoroutinefunction

from channels.db import database_sync_to_async as convert_to_async

from conreq import config

# pylint: disable=import-outside-toplevel

# TODO: All the default views in core will need to be made async, after more broad Django async support.
# Specifically, Django support for async decorators, template rendering, and ORM queries.


async def _render_view(view, request, *args, **kwargs):
    # Async Class View
    if getattr(view, "view_is_async", False):
        return await view.as_view()(request, *args, **kwargs)
    # Sync Class View
    if hasattr(view, "as_view"):
        async_cbv = convert_to_async(view.as_view())
        return await async_cbv(request, *args, **kwargs)
    # Async Function View
    if iscoroutinefunction(view):
        return await view(request, *args, **kwargs)
    # Sync Function View
    return await convert_to_async(view)(request, *args, **kwargs)


async def landing(request, *args, **kwargs):
    """Configurable landing view."""
    view = config.views.landing
    if view is None:
        from conreq._core.landing import views

        view = views.landing
    return await _render_view(view, request, *args, **kwargs)


async def home(request, *args, **kwargs):
    """Configurable home view."""
    view = config.views.home
    if view is None:
        from conreq._core.home import views

        view = views.home
    return await _render_view(view, request, *args, **kwargs)


async def sign_up(request, *args, **kwargs):
    """Configurable sign up view."""
    view = config.views.sign_up
    if view is None:
        from conreq._core.sign_up import views

        view = views.sign_up
    return await _render_view(view, request, *args, **kwargs)


async def sign_in(request, *args, **kwargs):
    """Configurable sign in view."""
    view = config.views.sign_in
    if view is None:
        from conreq._core.sign_in import views

        view = views.sign_in
    return await _render_view(view, request, *args, **kwargs)


async def edit_user(request, *args, **kwargs):
    """Configurable edit user view."""
    view = config.views.edit_user
    if view is None:
        from conreq._core.user_management import views

        view = views.EditUserView
    return await _render_view(view, request, *args, **kwargs)


async def delete_user(request, *args, **kwargs):
    """Configurable edit user view."""
    view = config.views.delete_user
    if view is None:
        from conreq._core.user_management import views

        view = views.DeleteUserView
    return await _render_view(view, request, *args, **kwargs)


async def password_reset(request, *args, **kwargs):
    """Configurable password reset view."""
    view = config.views.password_reset
    if view is None:
        from conreq._core.password_reset import views

        view = views.PasswordResetView
    return await _render_view(view, request, *args, **kwargs)


async def password_reset_sent(request, *args, **kwargs):
    """Configurable password reset sent view."""
    view = config.views.password_reset_sent
    if view is None:
        from conreq._core.password_reset import views

        view = views.PassWordResetSentView
    return await _render_view(view, request, *args, **kwargs)


async def password_reset_confirm(request, *args, **kwargs):
    """Configurable password reset confirmation view."""
    view = config.views.password_reset_confirm
    if view is None:
        from conreq._core.password_reset import views

        view = views.PasswordResetConfirmView
    return await _render_view(view, request, *args, **kwargs)


async def offline(request, *args, **kwargs):
    """Configurable offline view."""
    view = config.views.offline
    if view is None:
        from conreq._core.pwa import views

        view = views.offline
    return await _render_view(view, request, *args, **kwargs)


async def service_worker(request, *args, **kwargs):
    """Configurable service worker view."""
    view = config.views.service_worker
    if view is None:
        from conreq._core.pwa import views

        view = views.service_worker
    return await _render_view(view, request, *args, **kwargs)


async def web_manifest(request, *args, **kwargs):
    """Configurable web manifest view."""
    view = config.views.web_manifest
    if view is None:
        from conreq._core.pwa import views

        view = views.web_manifest
    return await _render_view(view, request, *args, **kwargs)
