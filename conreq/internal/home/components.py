import idom
from django.utils.text import slugify
from idom.html import button, div, i, nav, span

import conreq
from conreq.app.selectors import Modal, Viewport
from conreq.utils.components import authenticated
from conreq.utils.environment import get_debug, get_safe_mode

DEBUG = get_debug()
SAFE_MODE = get_safe_mode()

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
USERNAME_CONTAINER = {"className": "username-container"}
USERNAME = {"className": "username ellipsis"}
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
NAV_TAB = {"className": "nav-tab clickable"}
NAV_TAB_ACTIVE = {"className": "nav-tab clickable active"}
TAB_NAME = {"className": "tab-name ellipsis"}

# Modal
MODAL_CONTAINER = {
    "id": "modal-container",
    "className": "modal fade",
    "tabIndex": "-1",
    "role": "dialog",
    "style": {"display": "none"},
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
VIEWPORT_CONTAINER_PRIMARY = {"className": "viewport-container primary"}
VIEWPORT_CONTAINER_SECONDARY = {"className": "viewport-container secondary"}
VIEWPORT_CONTAINER_LOADING = {"className": "viewport-container loading"}

# Generic rules
HIDDEN = {"hidden": "hidden"}

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
SIDEBAR_SAFE_MODE = div(
    {
        "style": {
            "display": "flex",
            "align-items": "center",
            "justify-content": "center",
            "padding": "10px",
            "background": "red",
            "color": "#FFF",
            "font-weight": "700",
        }
    },
    "SAFE MODE",
)

# TODO: Add the following react components: SimpleBar, Pretty-Checkbox, IziToast, Bootstrap


@idom.component
@authenticated()
def homepage(websocket):
    state, set_state = idom.hooks.use_state(
        {
            "page_title": "Loading...",
            "viewport": Viewport.loading,
            "viewport_padding": True,
            "viewport_primary": None,
            "viewport_secondary": None,
            "modal": Modal.loading,
            "modal_title": "Loading...",
            "modal_header": None,
            "modal_body": None,
            "modal_footer": None,
        }
    )
    return div(
        navbar(websocket, state, set_state),
        modal(websocket, state, set_state),
        sidebar(websocket, state, set_state),
        viewport_loading(websocket, state, set_state),
        viewport_primary(websocket, state, set_state),
        viewport_secondary(websocket, state, set_state),
    )


@idom.component
def sidebar(websocket, state, set_state):
    if not websocket.scope["user"].is_authenticated:
        return None

    all_tabs = conreq.config.nav_tabs.items()

    return nav(
        SIDEBAR,
        *([SIDEBAR_SAFE_MODE] if SAFE_MODE else []),
        div(
            SIDEBAR_USER,
            div(USER_PIC, i(USER_PIC_PLACEHOLDER)),
            div(
                USERNAME_CONTAINER,
                div(USERNAME, websocket.scope["user"].get_username()),
            ),
        ),
        div(
            NAVIGATION,
            *(  # App tabs
                sidebar_group(websocket, state, set_state, group_name, group_values)
                for group_name, group_values in all_tabs
                if group_name not in {"User", "Admin", "Debug"}
            ),
            *(  # User tabs
                sidebar_group(websocket, state, set_state, group_name, group_values)
                for group_name, group_values in all_tabs
                if group_name == "User"
            ),
            *(  # Admin tabs
                sidebar_group(websocket, state, set_state, group_name, group_values)
                for group_name, group_values in all_tabs
                if group_name == "Admin" and websocket.scope["user"].is_staff
            ),
            *(  # Debug tabs
                sidebar_group(websocket, state, set_state, group_name, group_values)
                for group_name, group_values in all_tabs
                if group_name == "Debug" and websocket.scope["user"].is_staff and DEBUG
            ),
        ),
    )


def nav_tab_properties(websocket, state, set_state, tab):
    # pylint: disable=unused-argument
    if (
        state["viewport"] is not Viewport.loading
        and tab["component"] is state[f'viewport_{state["viewport"]}']
    ):
        return NAV_TAB_ACTIVE
    return NAV_TAB


def sidebar_tab(websocket, state, set_state, tab):
    return div(
        nav_tab_properties(websocket, state, set_state, tab)
        | {
            "onClick": lambda x: set_state(
                state
                | {
                    "viewport": tab["viewport"],
                    f'viewport_{tab["viewport"]}': tab["component"],
                    "viewport_padding": tab["viewport_padding"],
                }
            )
            if not tab["on_click"]
            else tab["on_click"](websocket, state, set_state, tab)
        },
        div(TAB_NAME, tab["name"]),
    )


def sidebar_group(websocket, state, set_state, group_name, group_values):
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
            div(TABS, *(sidebar_tab(websocket, state, set_state, tab) for tab in tabs)),
        ),
    )


@idom.component
def viewport_loading(websocket, state, set_state):
    # pylint: disable=unused-argument
    return div(
        VIEWPORT_CONTAINER_LOADING
        | ({} if state["viewport"] == Viewport.loading else HIDDEN),
        conreq.config.loading_animation_vdom,
    )


@idom.component
def viewport_primary(websocket, state, set_state):
    # pylint: disable=unused-argument
    return div(
        VIEWPORT_CONTAINER_PRIMARY
        | ({} if state["viewport"] == Viewport.primary else HIDDEN)
        | (
            {}
            if state["viewport_padding"] and state["viewport"] == Viewport.primary
            else {"className": VIEWPORT_CONTAINER_PRIMARY["className"] + " no-padding"}
        ),
        *(
            [state["viewport_primary"](websocket, state, set_state)]
            if state["viewport_primary"]
            else []
        ),
    )


@idom.component
def viewport_secondary(websocket, state, set_state):
    # pylint: disable=unused-argument
    return div(
        VIEWPORT_CONTAINER_SECONDARY
        | ({} if state["viewport"] == Viewport.secondary else HIDDEN)
        | (
            {}
            if state["viewport_padding"] and state["viewport"] == Viewport.secondary
            else {
                "className": VIEWPORT_CONTAINER_SECONDARY["className"] + " no-padding"
            }
        ),
        *(
            [state["viewport_secondary"](websocket, state, set_state)]
            if state["viewport_secondary"]
            else []
        ),
    )


@idom.component
def navbar(websocket, state, set_state):
    # pylint: disable=unused-argument
    return div(
        NAVBAR,
        button(
            NAVBAR_TOGGLER,
            span(NAVBAR_TOGGLER_ICON),
        ),
        div(NAVBAR_BRAND, state["page_title"]),
    )


@idom.component
def modal(websocket, state, set_state):
    return div(
        MODAL_CONTAINER,
        div(
            MODAL_DIALOG,
            div(
                MODAL_CONTENT,
                modal_head(websocket, state, set_state),
                modal_body(websocket, state, set_state),
                modal_footer(websocket, state, set_state),
            ),
        ),
    )


def modal_head(websocket, state, set_state):
    # pylint: disable=unused-argument
    if state["modal"] == Modal.show and state["modal_header"]:
        return state["modal_header"]
    return div(
        MODAL_HEADER,
        div(MODAL_HEADER_BTN_CONTAINER, MODAL_CLOSE_BTN),
        div(MODAL_TITLE, state["modal_title"]),
    )


def modal_body(websocket, state, set_state):
    # pylint: disable=unused-argument
    if state["modal"] == Modal.show and state["modal_body"]:
        return state["modal_body"]
    return div(
        MODAL_BODY,
        div({"className": "loading"}, conreq.config.loading_animation_vdom),
    )


def modal_footer(websocket, state, set_state):
    # pylint: disable=unused-argument
    if state["modal"] == Modal.show and state["modal_footer"]:
        return state["modal_footer"]
    return div(MODAL_FOOTER)
