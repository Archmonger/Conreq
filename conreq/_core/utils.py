from typing import Callable

from conreq import AuthLevel, NavTab, Viewport, ViewportSelector


def tab_constructor(
    name: str,
    component: Callable,
    on_click: Callable = None,  # TODO: document args = event, websocket, state, set_state, tab
    padding: bool = True,
    selector: ViewportSelector = ViewportSelector.primary,
    auth: AuthLevel = AuthLevel.user,
) -> NavTab:
    return NavTab(
        name=name,
        viewport=Viewport(
            component=component,
            selector=selector,
            padding=padding,
            auth=auth,
        ),
        on_click=on_click,
        auth=auth,
    )
