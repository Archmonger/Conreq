import idom
from django.utils.text import slugify
from idom.html import a, div, i, nav

from conreq import app

SIDEBAR = {
    "id": "sidebar",
    "class": "sidebar no-hightlighting collapsed",
    "data-aos": "fade-right",
    "data-aos-duration": "1000",
}
SIDEBAR_USER = {"class": "sidebar-user clickable"}
USER_PIC = {"class": "sidebar-profile-pic"}
USER_PIC_PLACEHOLDER = {"class": "fas fa-user"}
USERNAME = {"class": "username"}
ELLIPSIS = {"class": "ellipsis"}
NAVIGATION = {"id": "navigation"}
NAVGROUP = {
    "class": "nav-group clickable",
    "data-bs-toggle": "collapse",
    "aria-expanded": "true",
}
GROUP_NAME = {"class": "group-name ellipsis"}
GROUP_ICON = {"class": "group-icon"}
EXAMPLE_GROUP_ICON = {"class": "fas fa-user icon-left"}
GROUP_CARET = {"class": "fas fa-caret-up icon-right"}
TABS_COLLAPSE = {
    "class": "tabs-collapse collapse show",
}
TABS_INDICATOR = {"class": "tabs-indicator"}
TABS = {"class": "tabs"}
NAV_TAB = {"class": "nav-tab"}


@idom.component
def sidebar(websocket):
    if not websocket.scope["user"].is_authenticated:
        return None

    all_tabs = app.config.nav_tabs.items()

    return nav(
        SIDEBAR,
        div(
            SIDEBAR_USER,
            div(USER_PIC, i(USER_PIC_PLACEHOLDER)),
            div(USERNAME, div(ELLIPSIS, websocket.scope["user"].get_username())),
        ),
        div(
            NAVIGATION,
            *(  # App tabs
                sidebar_group(group_name, group_values)
                for group_name, group_values in all_tabs
                if group_name not in {"User", "Admin"}
            ),
            *(  # User tabs
                sidebar_group(group_name, group_values)
                for group_name, group_values in all_tabs
                if group_name == "User"
            ),
            *(  # Admin tabs
                sidebar_group(group_name, group_values)
                for group_name, group_values in all_tabs
                if group_name == "Admin" and websocket.scope["user"].is_staff
            ),
        ),
    )


def sidebar_group_icon(icon):
    if not icon:
        return i({"class": "far fa-circle"})

    return i("a")


def sidebar_tabs(tabs):
    return (
        div(
            NAV_TAB,
            a(ELLIPSIS, tab["name"]),
        )
        for tab in tabs
    )


def sidebar_group(group_name, group_values):
    group_icon = group_values["icon"]
    tabs = group_values["tabs"]
    group_id = f"{slugify(group_name)}-tabs"

    return (
        div(
            NAVGROUP
            | {
                "data-bs-target": f"#{group_id}",
                "aria-controls": group_id,
                "title": group_name,
            },
            div(
                GROUP_NAME,
                div(GROUP_ICON, sidebar_group_icon(group_icon)),
                group_name,
            ),
            i(GROUP_CARET | {"title": f'Collapse the "{group_name}" group.'}),
        ),
        div(
            TABS_COLLAPSE | {"id": group_id},
            div(TABS_INDICATOR),
            div(TABS, *sidebar_tabs(tabs)),
        ),
    )
