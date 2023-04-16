from typing import Callable, Literal

from reactpy.core.component import Component

from conreq import config


def user_management(
    component: Callable[..., Component] | None = None,
    selector: Literal[
        "main",
        "manage_users",
        "edit_user",
        "delete_user",
        "manage_invites",
        "create_invite",
    ] = "main",
):
    """Changes the manage users component."""
    setattr(config.components.user_management, selector, component)
    return component


def server_settings(
    component: Callable[..., Component] | None = None,
    selector: Literal[
        "main", "general", "styling", "webserver", "email", "system_info"
    ] = "main",
):
    """Changes the server settings component."""
    setattr(config.components.server_settings, selector, component)
    return component


def user_settings(
    component: Callable[..., Component] | None = None,
    selector: Literal["main", "general", "change_password", "delete_account"] = "main",
):
    """Changes the user settings component."""
    setattr(config.components.user_settings, selector, component)
    return component


def app_store(
    component: Callable[..., Component] | None = None,
    selector: Literal["main"] = "main",
):
    """Changes the app store component."""
    # TODO: Add more selectors after fleshing out the app store tab
    setattr(config.components.app_store, selector, component)
    return component


def loading_animation(
    component: Callable[..., Component] | None = None,
    selector: Literal["small", "large"] = "large",
):
    """Changes the default component loading animation."""
    if component:
        setattr(config.components.loading_animation, selector, component)
    return component
