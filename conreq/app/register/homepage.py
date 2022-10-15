from typing import Callable

from idom.core.component import Component

from conreq import config
from conreq.types import (
    CSS,
    SCSS,
    AuthLevel,
    HTMLTemplate,
    JavaScript,
    NavGroup,
    SidebarTab,
    Viewport,
)


def sidebar_tab(
    name: str,
    group: NavGroup,
    on_click: Callable | None = None,
    html_class: str = "",
    padding: bool = True,
    auth: str = AuthLevel.user,
) -> Callable:
    """Decorates an IDOM component. Tab is added to the sidebar and is rendered when clicked.
    By default, the function decorated will be rendered to the viewport. The `on_click` event
    can be overridden to change this behavior."""
    # TODO: Implement auth level
    # TODO: URL support (Requires IDOM to support URL routing)

    def decorator(component: Component):
        if group not in config.homepage.sidebar_tabs:
            config.homepage.sidebar_tabs.add(group)

        for nav_group in config.homepage.sidebar_tabs:
            if group == nav_group:
                group.tabs.add(
                    SidebarTab(
                        name=name,
                        viewport=Viewport(
                            component=component,
                            html_class=html_class,
                            padding=padding,
                        ),
                        on_click=on_click,
                        auth=auth,
                    )
                )
                break

        return component

    return decorator


def sidebar_group(group: NavGroup):
    """Creates a nav group and/or sets the group icon."""
    for nav_group in config.homepage.sidebar_tabs:
        if group == nav_group:
            nav_group.icon = group.icon
            return

    config.homepage.sidebar_tabs.add(group)


def css(file_link: CSS):
    if file_link.local:
        config.homepage.local_stylesheets.append(file_link)
    else:
        config.homepage.remote_stylesheets.append(file_link)


def scss(file_link: SCSS):
    config.homepage.scss_stylesheets.append(file_link)


def javascript(file_link: JavaScript):
    if file_link.local:
        config.homepage.local_scripts.append(file_link)
    else:
        config.homepage.remote_scripts.append(file_link)


def head_content(template: HTMLTemplate):
    config.homepage.head_content.append(template)
