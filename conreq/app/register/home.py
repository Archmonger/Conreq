from functools import wraps
from typing import Callable

import conreq
from conreq.app.components.icon import Icon

from ..selectors import AuthLevel, Viewport


def nav_tab(
    tab_name: str,
    group_name: str,
    group_icon: Icon = None,
    tab_icon: Icon = None,
    viewport: Viewport = Viewport.primary,
    on_click: Callable = None,  # Args = websocket, state, set_state, tab
    auth_level: AuthLevel = AuthLevel.user,
    padding: bool = True,
) -> Callable:
    """Decorates an IDOM component. Tab is added to the sidebar and is rendered when clicked.
    By default, the function decorated will be rendered to the viewport. The `on_click` event
    can be overridden to change this behavior."""

    nav_tabs = conreq.config.nav_tabs
    group = nav_tabs.get(group_name)

    if not group:
        nav_tabs[group_name] = {"icon": group_icon, "tabs": []}
        group = nav_tabs[group_name]

    def decorator(func):
        group["tabs"].append(
            {
                "name": tab_name,
                "viewport": viewport,
                "viewport_padding": padding,
                "on_click": on_click,
                "auth": auth_level,
                "icon": tab_icon,
                "component": func,
            }
        )

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def nav_group(
    group_name: str,
    group_icon: Icon = None,
):
    """Creates a nav group and/or sets the group icon."""
    nav_tabs = conreq.config.nav_tabs
    group = nav_tabs.get(group_name)

    if not group:
        nav_tabs[group_name] = {"icon": group_icon, "tabs": []}

    else:
        nav_tabs[group_name].update("icon", group_icon)


def server_settings(page_name: str) -> Callable:
    """Decorates an IDOM component. Creates a settings page."""

    server_setting_tabs = conreq.config.server_setting_tabs

    def decorator(func):
        server_setting_tabs[page_name] = {"component": func}

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator
