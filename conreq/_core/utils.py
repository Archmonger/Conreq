from typing import Callable

from conreq import AuthLevel, Viewport


def tab_constructor(
    tab_name: str,
    component: Callable,
    on_click: Callable = None,  # TODO: document args = websocket, state, set_state, tab
    padding: bool = True,
    viewport: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
):
    return {
        "name": tab_name,
        "viewport": viewport,
        "viewport_padding": padding,
        "on_click": on_click,
        "auth": auth_level,
        "component": component,
    }
