import idom
from django.utils.text import slugify
from idom.html import div, i, nav

from conreq import config
from conreq.app.selectors import Viewport
from conreq.utils.environment import get_debug, get_safe_mode

DEBUG = get_debug()
SAFE_MODE = get_safe_mode()
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
NAV_GROUP = {
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
DEFAULT_NAV_GROUP_ICON = i({"className": "far fa-circle"})
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
USER_ADMIN_DEBUG = ("User", "Admin", "Debug")


@idom.component
def sidebar(websocket, state, set_state):
    if not websocket.scope["user"].is_authenticated:
        return None

    all_tabs = config.homepage.nav_tabs.items()

    @idom.hooks.use_effect
    async def set_default_tab():
        if state["viewport"] != Viewport.initial:
            return None

        # Use the configured default tab, if it exists
        if config.homepage.default_nav_tab:
            set_state(
                state
                | {
                    "viewport": Viewport.primary,
                    "viewport_primary": config.homepage.default_nav_tab,
                    "viewport_padding": True,
                }
            )
            return None

        # Select the top most tab, if it exists
        for group_name, group_values in all_tabs:
            if not group_values["tabs"] or group_name in USER_ADMIN_DEBUG:
                continue
            tab = group_values["tabs"][0]
            set_state(
                state
                | {
                    "viewport": tab["viewport"],
                    f'viewport_{tab["viewport"]}': tab["component"],
                    "viewport_padding": tab["viewport_padding"],
                }
            )
            return None

    return nav(
        SIDEBAR,
        *([SIDEBAR_SAFE_MODE] if SAFE_MODE else []),
        div(
            SIDEBAR_USER
            | {
                "onClick": lambda x: set_state(
                    state
                    | {
                        "viewport": Viewport.primary,
                        "viewport_primary": config.components.user_settings,
                        "viewport_padding": True,
                    }
                )
            },
            div(USER_PIC, i(USER_PIC_PLACEHOLDER)),
            div(
                USERNAME_CONTAINER,
                div(USERNAME, websocket.scope["user"].get_username()),
            ),
        ),
        div(
            # pylint: disable=protected-access
            NAVIGATION,
            *(  # App tabs
                sidebar_group(websocket, state, set_state, group_name, group_values)
                for group_name, group_values in all_tabs
                if group_name not in USER_ADMIN_DEBUG
            ),
            *(  # User tabs
                sidebar_group(
                    websocket,
                    state,
                    set_state,
                    group_name,
                    group_values,
                    bottom_tabs=config._homepage.user_nav_tabs,
                )
                for group_name, group_values in all_tabs
                if group_name == "User"
            ),
            *(  # Admin tabs
                sidebar_group(
                    websocket,
                    state,
                    set_state,
                    group_name,
                    group_values,
                    bottom_tabs=config._homepage.admin_nav_tabs,
                )
                for group_name, group_values in all_tabs
                if group_name == "Admin" and websocket.scope["user"].is_staff
            ),
            *(  # Debug tabs
                sidebar_group(
                    websocket,
                    state,
                    set_state,
                    group_name,
                    group_values,
                    top_tabs=config._homepage.debug_nav_tabs,
                )
                for group_name, group_values in all_tabs
                if group_name == "Debug" and websocket.scope["user"].is_staff and DEBUG
            ),
        ),
    )


def nav_tab_class(state, tab):
    if (
        state["viewport"] not in {Viewport.loading, Viewport.initial}
        and tab["component"] is state[f'viewport_{state["viewport"]}']
    ):
        return NAV_TAB_ACTIVE
    return NAV_TAB


def sidebar_tab(websocket, state, set_state, tab):
    return div(
        nav_tab_class(state, tab)
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


def sidebar_group(
    websocket,
    state,
    set_state,
    group_name,
    group_values,
    top_tabs=None,
    bottom_tabs=None,
):
    icon = group_values["icon"]
    tabs = group_values["tabs"]
    _top_tabs = top_tabs or []
    _bottom_tabs = bottom_tabs or []
    tabs_id = f"{slugify(group_name)}-tabs"

    return (
        div(
            NAV_GROUP
            | {
                "data-bs-target": f"#{tabs_id}",
                "aria-controls": tabs_id,
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
            TABS_COLLAPSE | {"id": tabs_id},
            div(TABS_INDICATOR),
            div(
                TABS,
                *(sidebar_tab(websocket, state, set_state, tab) for tab in _top_tabs),
                *(sidebar_tab(websocket, state, set_state, tab) for tab in tabs),
                *(
                    sidebar_tab(websocket, state, set_state, tab)
                    for tab in _bottom_tabs
                ),
            ),
        ),
    )
