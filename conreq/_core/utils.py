from typing import Callable

from conreq import AuthLevel, NavTab, Viewport, ViewportSelector


def tab_constructor(
    name: str,
    component: Callable,
    on_click: Callable = None,  # TODO: document args = event, websocket, state, set_state, tab
    padding: bool = True,
    selector: ViewportSelector = ViewportSelector.auto,
    auth: AuthLevel = AuthLevel.user,
    html_class: str = "",
) -> NavTab:
    return NavTab(
        name=name,
        viewport=Viewport(
            component=component,
            selector=selector,
            html_class=html_class,
            padding=padding,
            auth=auth,
        ),
        on_click=on_click,
        auth=auth,
    )
