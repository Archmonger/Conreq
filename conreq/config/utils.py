from typing import Callable

from conreq.types import AuthLevel, SidebarTab, Viewport


def tab_constructor(
    name: str,
    component: Callable,
    on_click: Callable | None = None,
    padding: bool = True,
    auth: str = AuthLevel.user,
    html_class: str = "",
) -> SidebarTab:
    return SidebarTab(
        name=name,
        viewport=Viewport(
            component=component,
            html_class=html_class,
            padding=padding,
        ),
        on_click=on_click,
        auth=auth,
    )
