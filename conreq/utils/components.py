from functools import wraps
from typing import Callable

import idom
from django.urls import path, re_path
from idom.core.proto import VdomDict
from idom.core.vdom import make_vdom_constructor
from idom.html import div, li, ul

from conreq.utils.environment import get_base_url

BASE_URL = get_base_url(append_slash=False, prepend_slash=False)
if BASE_URL:
    BASE_URL = BASE_URL + "/"
iframe = make_vdom_constructor("iframe")


def authenticated(
    fallback: str = None,
) -> Callable:
    """Decorates an IDOM component."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(websocket, *args, **kwargs):
            return (
                func(websocket, *args, **kwargs)
                if websocket.scope["user"].is_authenticated
                else fallback or div()
            )

        return _wrapped_func

    return decorator


# TODO: Use Django resolve and raise an exception if registering something that already exists
def django_to_idom(
    url_pattern: str = None,
    name: str = None,
    use_regex: bool = False,
) -> VdomDict:
    """Converts a Django view function/class into an IDOM component
    by turning it into an idom component in an iframe."""

    def decorator(func: Callable):
        # pylint: disable=import-outside-toplevel
        from conreq.urls import urlpatterns
        from conreq.utils.profiling import profiled_view

        # Register a new URL path
        view = profiled_view(func)
        dotted_path = f"{func.__module__}.{func.__name__}"
        view_name = name or dotted_path
        src_url = url_pattern or f"{BASE_URL}iframe/{dotted_path}".replace(
            "<", ""
        ).replace(">", "")

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
def tabbed_viewport(websocket, tabs):
    """Generates a viewport with the provided tabs. Viewport functions should accept
    `websocket, state, set_state` as arguements."""
    state, set_state = idom.hooks.use_state(
        {"current_tab": tabs[next(iter(tabs))]["component"]}
    )

    return div(
        {"className": "tabbed-viewport-container"},
        div(
            {"className": "tabbed-viewport"},
            state["current_tab"](websocket, state, set_state),
        ),
        ul(
            {"className": "tabbed-viewport-selector list-group"},
            *_tabbed_viewport_tabs(tabs, state, set_state),
        ),
    )


def _tabbed_viewport_tabs(tabs: dict, state, set_state):
    return [
        li(
            _tabbed_viewport_tabs_values(tab_properties, state, set_state),
            tab_name,
        )
        for tab_name, tab_properties in tabs.items()
    ]


def _tabbed_viewport_tabs_values(tab_properties, state, set_state):
    return {
        "className": f"list-group-item clickable{' active' if state['current_tab'] is tab_properties['component'] else ''}",
        "onClick": lambda x: set_state(
            state | {"current_tab": tab_properties["component"]}
        ),
    }
