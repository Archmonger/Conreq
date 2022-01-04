from typing import Callable

from sortedcontainers import SortedList

from conreq import config
from conreq.app.selectors import AuthLevel, Viewport, ViewType
from conreq.app.types import Icon
from conreq.utils.components import view_to_component


# TODO: Implement url_pattern for IDOM components. Needs react-router to be integrated into IDOM core.
def nav_tab(
    tab_name: str,
    group_name: str,
    group_icon: Icon = None,
    on_click: Callable = None,  # TODO: document args = websocket, state, set_state, tab
    padding: bool = True,
    viewport: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
    view_type: ViewType = ViewType.component,
    url_pattern: str = None,  # For Django only (as of now)
    url_name: str = None,  # For Django only (as of now)
    url_regex: bool = False,  # For Django only (as of now)
) -> Callable:
    """Decorates an IDOM component. Tab is added to the sidebar and is rendered when clicked.
    By default, the function decorated will be rendered to the viewport. The `on_click` event
    can be overridden to change this behavior."""
    # TODO: Implement auth level
    # TODO: URL support (Requires IDOM to support URL routing)

    def decorator(func):
        if view_type == ViewType.component:
            component = func
        elif view_type == ViewType.view:
            component = view_to_component(
                url_pattern=url_pattern, name=url_name, use_regex=url_regex
            )(func)
        else:
            raise ValueError(f"Invalid nav tab view_type of '{view_type}'.")

        group = config.homepage.nav_tabs.setdefault(
            group_name,
            {"icon": group_icon, "tabs": SortedList(key=lambda x: x["name"])},
        )
        group["tabs"].add(
            {
                "name": tab_name,
                "viewport": viewport,
                "viewport_padding": padding,
                "on_click": on_click,
                "auth": auth_level,
                "component": component,
            }
        )

        return func

    return decorator


def nav_group(
    group_name: str,
    group_icon: Icon = None,
):
    """Creates a nav group and/or sets the group icon."""
    navbar = config.homepage.nav_tabs
    group = navbar.get(group_name)

    if not group:
        navbar[group_name] = {
            "icon": group_icon,
            "tabs": SortedList([], key=lambda x: x["name"]),
        }

    else:
        navbar[group_name]["icon"] = group_icon


def css(reverse_path: str, attributes: dict = None, local=True) -> None:
    if local:
        config.homepage.local_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )
    else:
        config.homepage.remote_stylesheets.append(
            {"path": reverse_path, "attributes": attributes}
        )


def scss(reverse_path: str, attributes: list[tuple] = None):
    config.homepage.scss_stylesheets.append(
        {"path": reverse_path, "attributes": attributes}
    )


def javascript(reverse_path: str, attributes: list[tuple] = None, local=True) -> None:
    if local:
        config.homepage.local_scripts.append(
            {"path": reverse_path, "attributes": attributes}
        )
    else:
        config.homepage.remote_scripts.append(
            {"path": reverse_path, "attributes": attributes}
        )


def font(reverse_path: str, attributes: list[tuple] = None, local=True) -> None:
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
