from functools import wraps
from typing import Callable

from conreq import config
from conreq.app.types import Icon
from conreq.utils.components import django_to_idom

from ..selectors import AuthLevel, Viewport, ViewType


# TODO: Implement url_pattern for IDOM components. Needs react-router to be integrated into IDOM core.
def nav_tab(
    tab_name: str,
    group_name: str,
    group_icon: Icon = None,
    on_click: Callable = None,  # TODO: document args = websocket, state, set_state, tab
    padding: bool = True,
    viewport: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
    view_type: ViewType = ViewType.idom,
    url_pattern: str = None,
    name: str = None,
    use_regex: bool = False,
) -> Callable:
    """Decorates an IDOM component. Tab is added to the sidebar and is rendered when clicked.
    By default, the function decorated will be rendered to the viewport. The `on_click` event
    can be overridden to change this behavior."""
    # TODO: Implement auth level
    # TODO: URL support (Requires IDOM to support URL routing)

    def decorator(func):

        if view_type == ViewType.idom:
            component = func
        elif view_type == ViewType.django:
            component = django_to_idom(
                url_pattern=url_pattern, name=name, use_regex=use_regex
            )(func)
        else:
            raise ValueError(f"Invalid nav tab view_type of '{view_type}'.")

        group = config.tabs.navbar.setdefault(
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
    navbar = config.tabs.navbar
    group = navbar.get(group_name)

    if not group:
        navbar[group_name] = {"icon": group_icon, "tabs": []}

    else:
        navbar[group_name].update("icon", group_icon)


def server_settings(page_name: str) -> Callable:
    """Decorates an IDOM component. Creates a settings page."""

    def decorator(func):
        config.tabs.server_settings[page_name] = {"component": func}

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator
