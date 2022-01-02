from functools import wraps
from typing import Callable, Optional, Union

import idom
from django.urls import path, re_path
from idom.core.proto import ComponentType, VdomDict
from idom.core.vdom import make_vdom_constructor
from idom.html import div, li, ul

from conreq.app.selectors import AuthLevel
from conreq.utils.environment import get_base_url
from conreq.utils.views import authenticated as authenticated_view

BASE_URL = get_base_url(append_slash=False, prepend_slash=False)
if BASE_URL:
    BASE_URL = BASE_URL + "/"
iframe = make_vdom_constructor("iframe")


def authenticated(
    fallback: Union[ComponentType, VdomDict] = None,
    auth_level: AuthLevel = AuthLevel.user,
) -> ComponentType:
    """Decorates an IDOM component."""

    def decorator(component):
        @wraps(component)
        def _wrapped_func(websocket, *args, **kwargs):
            if auth_level == AuthLevel.user:
                return (
                    component(websocket, *args, **kwargs)
                    if websocket.scope["user"].is_authenticated
                    else fallback or div()
                )
            if auth_level == AuthLevel.admin:
                return (
                    component(websocket, *args, **kwargs)
                    if websocket.scope["user"].is_staff
                    else fallback or div()
                )
            return component(websocket, *args, **kwargs)

        return _wrapped_func

    return decorator


# TODO: Use Django resolve and raise an exception if registering something that already exists
def view_to_component(
    url_pattern: str = None,
    name: str = None,
    use_regex: bool = False,
    auth_level: AuthLevel = AuthLevel.user,
) -> ComponentType:
    """Converts a Django view function/class into an IDOM component
    by turning it into an idom component in an iframe."""

    def decorator(func: Callable):
        # pylint: disable=import-outside-toplevel
        from conreq.urls import urlpatterns
        from conreq.utils.profiling import profiled_view

        # Register a new URL path
        view = profiled_view(authenticated_view(func, auth_level))
        dotted_path = f"{func.__module__}.{func.__name__}".replace("<", "").replace(
            ">", ""
        )
        view_name = name or dotted_path
        src_url = url_pattern or f"{BASE_URL}iframe/{dotted_path}"

        if use_regex:
            urlpatterns.append(re_path(src_url, view, name=view_name))
        else:
            urlpatterns.append(path(src_url, view, name=view_name))

        # Create an iframe with src=...
        @idom.component
        def idom_component(*args, **kwargs):
            return iframe({"src": src_url, "loading": "lazy"})

        return idom_component

    return decorator


@idom.component
def tabbed_viewport(
    websocket,
    state,
    set_state,
    tabs: dict,
    top_tabs: Optional[dict] = None,
    bottom_tabs: Optional[dict] = None,
    default_tab: Optional[Callable] = None,
):
    """Generates a viewport with the provided tabs. Viewport functions should accept
    `websocket, state, set_state` as arguements."""
    tab_state, set_tab_state = idom.hooks.use_state(
        {
            "current_tab": _default_tab(
                top_tabs, tabs, bottom_tabs, default_tab=default_tab
            )
        }
    )

    return div(
        {"className": "tabbed-viewport-container"},
        div(
            {"className": "tabbed-viewport"},
            tab_state["current_tab"](websocket, state, set_state),
        ),
        ul(
            {"className": "tabbed-viewport-selector list-group"},
            *_tabbed_viewport_tabs(top_tabs, tab_state, set_tab_state),
            *_tabbed_viewport_tabs(tabs, tab_state, set_tab_state),
            *_tabbed_viewport_tabs(bottom_tabs, tab_state, set_tab_state),
        ),
    )


def _default_tab(*tab_groups, default_tab=None):
    if default_tab:
        return default_tab

    for tabs in tab_groups:
        if tabs:
            return tabs[next(iter(tabs))]["component"]

    return None


def _tabbed_viewport_tabs(tabs: dict, tab_state, set_tab_state):
    if not tabs:
        return []

    return [
        li(
            _tabbed_viewport_tabs_values(tab_properties, tab_state, set_tab_state),
            tab_name,
        )
        for tab_name, tab_properties in tabs.items()
    ]


def _tabbed_viewport_tabs_values(tab_properties, tab_state, set_tab_state):
    return {
        "className": f"list-group-item clickable{' active' if tab_state['current_tab'] is tab_properties['component'] else ''}",
        "onClick": lambda x: set_tab_state(
            {"current_tab": tab_properties["component"]}
        ),
    }
