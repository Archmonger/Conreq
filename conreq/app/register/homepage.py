from typing import Callable

from conreq import config
from conreq.types import AuthLevel, Icon, NavGroup, SidebarTab, Viewport


def sidebar_tab(
    name: str,
    group_name: str,
    group_icon: Icon | None = None,
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

    def decorator(component):
        if group_name not in config.homepage.sidebar_tabs:
            config.homepage.sidebar_tabs.append(
                NavGroup(name=group_name, icon=group_icon)
            )

        for group in config.homepage.sidebar_tabs:
            if group_name == group:
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


def sidebar_group(
    name: str,
    icon: Icon | None = None,
):
    """Creates a nav group and/or sets the group icon."""
    for group in config.homepage.sidebar_tabs:
        if name == group:
            group.icon = icon
            return

    config.homepage.sidebar_tabs.add(NavGroup(name=name, icon=icon))


def css(reverse_path: str, attributes: dict | None = None, local=True) -> None:
    if local:
        config.homepage.local_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )
    else:
        config.homepage.remote_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )


def scss(reverse_path: str, attributes: list[tuple] | None = None):
    config.homepage.scss_stylesheets.append(
        {"path": reverse_path, "attributes": attributes}
    )


def javascript(
    reverse_path: str, attributes: list[tuple] | None = None, local=True
) -> None:
    if local:
        config.homepage.local_scripts.append(
            {"path": reverse_path, "attributes": attributes}
        )
    else:
        config.homepage.remote_scripts.append(
            {"path": reverse_path, "attributes": attributes}
        )


def font(reverse_path: str, attributes: list[tuple] | None = None, local=True) -> None:
    if local:
        config.homepage.local_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )
    else:
        config.homepage.remote_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )


def head_content(template: str) -> None:
    config.homepage.head_content.append(template)
