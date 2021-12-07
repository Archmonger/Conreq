from functools import wraps
from typing import Callable

import conreq
from conreq.app.components.icon import Icon
from conreq.utils.components import django_to_idom

from ..selectors import AuthLevel, Viewport, ViewType


def nav_tab(
    tab_name: str,
    group_name: str,
    group_icon: Icon = None,
    on_click: Callable = None,  # TODO: document args = websocket, state, set_state, tab
    padding: bool = True,
    viewport: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
    view_type: ViewType = ViewType.idom,
) -> Callable:
    """Decorates an IDOM component. Tab is added to the sidebar and is rendered when clicked.
    By default, the function decorated will be rendered to the viewport. The `on_click` event
    can be overridden to change this behavior."""
    # TODO: Implement auth level

    def decorator(func):

        if view_type == ViewType.idom:
            component = func
        elif view_type == ViewType.django:
            component = django_to_idom(func)
        else:
            raise ValueError(f"Invalid nav tab view_type of '{view_type}'.")

        group = conreq.config.nav_tabs.setdefault(
            group_name, {"icon": group_icon, "tabs": []}
        )
        group["tabs"].append(
            {
                "name": tab_name,
                "viewport": viewport,
                "viewport_padding": padding,
                "on_click": on_click,
                "auth": auth_level,
                "component": component,
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

    def decorator(func):
        conreq.config.server_setting_tabs[page_name] = {"component": func}

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator
