import idom
from django.utils.text import slugify
from idom.html import a, button, div, i, nav, span

from conreq import app

# Sidebar
SIDEBAR = {
    "id": "sidebar",
    "className": "sidebar no-hightlighting collapsed",
    "data-aos": "fade-right",
    "data-aos-duration": "1000",
}
SIDEBAR_USER = {"className": "sidebar-user clickable"}
USER_PIC = {"className": "sidebar-profile-pic"}
USER_PIC_PLACEHOLDER = {"className": "fas fa-user"}
USERNAME = {"className": "username"}
ELLIPSIS = {"className": "ellipsis"}
NAVIGATION = {"id": "navigation"}
NAVGROUP = {
    "className": "nav-group clickable",
    "data-bs-toggle": "collapse",
    "aria-expanded": "true",
}
GROUP_NAME = {"className": "group-name ellipsis"}
GROUP_ICON = {"className": "group-icon"}
EXAMPLE_GROUP_ICON = {"className": "fas fa-user icon-left"}
GROUP_CARET = {"className": "fas fa-caret-up icon-right"}
TABS_COLLAPSE = {
    "className": "tabs-collapse collapse show",
}
TABS_INDICATOR = {"className": "tabs-indicator"}
TABS = {"className": "tabs"}
NAV_TAB = {"className": "nav-tab"}

# Modal
MODAL_CONTAINER = {
    "id": "modal-container",
    "className": "modal fade",
    "tabIndex": "-1",
    "role": "dialog",
    "aria-hidden": "true",
}
MODAL_DIALOG = {
    "id": "modal-dialog",
    "className": "modal-dialog modal-dialog-centered modal-lg",
    "role": "document",
}
MODAL_CONTENT = {"id": "modal-content", "className": "modal-content"}
MODAL_HEADER = {"className": "modal-header"}
MODAL_HEADER_BTN_CONTAINER = {
    "className": "modal-header-btn-container",
    "data-bs-dismiss": "modal",
    "aria-label": "Close",
}
MODAL_TITLE = {"className": "title"}
MODAL_BODY = {"className": "modal-body loading"}
MODAL_FOOTER = {"className": "modal-footer"}

# Viewport
VIEWPORT_CONTAINER = {"className": "viewport-container", "hidden": "hidden"}
VIEWPORT_CONTAINER_LOADING = {"className": "viewport-container-loading"}

# Navbar
NAVBAR = {"className": "navbar navbar-expand-md navbar-dark", "data-aos": "fade-down"}
NAVBAR_TOGGLER = {
    "className": "navbar-toggler",
    "type": "button",
    "aria-label": "Toggle sidebar",
    "title": "Toggle sidebar",
}
NAVBAR_TOGGLER_ICON = {"className": "navbar-toggler-icon"}
NAVBAR_BRAND = {"className": "navbar-brand ellipsis"}

# Generic VDOM
DEFAULT_NAV_GROUP_ICON = i({"className": "far fa-circle"})
MODAL_CLOSE_BTN = i(
    {
        "title": "Close",
        "className": "fas fa-window-close clickable",
    }
)


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


@idom.component
def viewport_loading_animation(websocket):
    return div(
        VIEWPORT_CONTAINER_LOADING,
        app.config.loading_animation_vdom,
    )


@idom.component
def viewport(websocket):
    return div(VIEWPORT_CONTAINER)


@idom.component
def navbar(websocket):
    return div(
        NAVBAR,
        button(
            NAVBAR_TOGGLER,
            span(NAVBAR_TOGGLER_ICON),
        ),
        div(NAVBAR_BRAND, "Loading..."),
    )


@idom.component
def modal(websocket):
    return div(
        MODAL_CONTAINER,
        div(
            MODAL_DIALOG,
            div(
                MODAL_CONTENT,
                div(
                    MODAL_HEADER,
                    div(MODAL_HEADER_BTN_CONTAINER, MODAL_CLOSE_BTN),
                    div(MODAL_TITLE, "Loading..."),
                ),
                div(
                    MODAL_BODY,
                    div({"className": "loading"}, app.config.loading_animation_vdom),
                ),
                div(MODAL_FOOTER),
            ),
        ),
    )


def sidebar_tabs(tabs):
    return (
        div(
            NAV_TAB,
            a(ELLIPSIS, tab["name"]),
        )
        for tab in tabs
    )


def sidebar_group(group_name, group_values):
    icon = group_values["icon"]
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
                div(GROUP_ICON, DEFAULT_NAV_GROUP_ICON if not icon else icon),
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
