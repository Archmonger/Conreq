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

        group = config.homepage.nav_tab.setdefault(
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

        return func

    return decorator


def nav_group(
    group_name: str,
    group_icon: Icon = None,
):
    """Creates a nav group and/or sets the group icon."""
    navbar = config.homepage.nav_tab
    group = navbar.get(group_name)

    if not group:
        navbar[group_name] = {"icon": group_icon, "tabs": []}

    else:
        navbar[group_name].update("icon", group_icon)


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
