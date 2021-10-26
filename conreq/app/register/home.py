from functools import wraps
from typing import Callable

from conreq import app
from conreq.app.component.icon import Icon

from ..selectors import AuthLevel, Viewport


def nav_tab(
    group_name: str,
    tab_name: str,
    group_icon: Icon = None,
    tab_icon: Icon = None,
    selector: Viewport = Viewport.primary,  # TODO: Can be viewport, modal, or none
    auth_level: AuthLevel = AuthLevel.user,
) -> Callable:
    """Decorates an IDOM component. Tab is added to the sidebar and is rendered when clicked."""

    nav_tabs = app.config.nav_tabs
    group = nav_tabs.get(group_name)

    if not group:
        nav_tabs[group_name] = {"icon": group_icon, "tabs": []}
        group = nav_tabs[group_name]

    def decorator(func):
        group["tabs"].append(
            {
                "name": tab_name,
                "selector": selector,
                "auth": auth_level,
                "icon": tab_icon,
                "component": func,
            }
        )

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator


def server_setting(page_name: str) -> Callable:
    """Decorates an IDOM component. Creates a settings page."""

    server_setting_tabs = app.config.server_setting_tabs

    def decorator(func):

        server_setting_tabs.append({"name": page_name, "component": func})

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator
