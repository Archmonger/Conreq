from copy import copy

import idom
from idom.html import div, i, nav

from conreq import HomepageState, Viewport, ViewportSelector, config, NavTab
from conreq.utils.environment import get_debug, get_safe_mode
from conreq.utils.generic import clean_string

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


# TODO: Add event history tab. Admin group. Database backed.
# TODO: Add DB backup, media backup, and clear cache somewhere in the admin group
@idom.component
def sidebar(websocket, state: HomepageState, set_state):
    if not websocket.scope["user"].is_authenticated:
        return None

    all_tabs = config.homepage.nav_tabs.items()

    @idom.hooks.use_effect
    async def set_default_tab():
        if state.viewport_selector != ViewportSelector.initial:
            return None

        # Use the configured default tab, if it exists
        if config.homepage.default_nav_tab:
            state.viewport_selector = config.homepage.default_nav_tab.viewport.selector
            state.viewport_primary = config.homepage.default_nav_tab.viewport
            set_state(copy(state))
            return None

        # Select the top most tab, if it exists
        for group_name, group_values in all_tabs:
            if not group_values["tabs"] or group_name in USER_ADMIN_DEBUG:
                continue
            tab: NavTab = group_values["tabs"][0]
            state.viewport_selector = tab.viewport.selector
            if tab["viewport"] == ViewportSelector.primary:
                state.viewport_primary = tab.viewport
            if tab.viewport.selector == ViewportSelector.secondary:
                state.viewport_secondary = tab.viewport
            set_state(copy(state))
            return None

    async def username_on_click(_):
        state.viewport_selector = ViewportSelector.primary
        state.viewport_primary = Viewport(config.components.user_settings)
        set_state(copy(state))

    return nav(
        SIDEBAR,
        *([SIDEBAR_SAFE_MODE] if SAFE_MODE else []),
        div(
            SIDEBAR_USER | {"onClick": username_on_click},
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


def nav_tab_class(state: HomepageState, tab: NavTab):
    if state.viewport_selector not in {
        ViewportSelector.loading,
        ViewportSelector.initial,
    } and tab.viewport.component is state.__getattribute__(
        f"viewport_{state.viewport_selector}"
    ):
        return NAV_TAB_ACTIVE
    return NAV_TAB


def sidebar_tab(websocket, state: HomepageState, set_state, tab: NavTab):
    async def on_click(_):
        state.viewport_selector = tab.viewport.selector
        if tab.viewport.selector == ViewportSelector.primary:
            state.viewport_primary = tab.viewport
        if tab.viewport.selector == ViewportSelector.secondary:
            state.viewport_secondary = tab.viewport
        set_state(copy(state))

    return div(
        nav_tab_class(state, tab)
        | {
            "onClick": on_click
            if not tab.on_click
            else tab.on_click(websocket, state, set_state, tab)
        },
        div(TAB_NAME, tab.name),
    )


def sidebar_group(
    websocket,
    state: HomepageState,
    set_state,
    group_name,
    group_values,
    top_tabs: list[NavTab] = None,
    bottom_tabs: list[NavTab] = None,
):
    icon = group_values["icon"]
    tabs = group_values["tabs"]
    _top_tabs = top_tabs or []
    _bottom_tabs = bottom_tabs or []
    group_name_clean = clean_string(group_name, lowercase=False)
    group_id = f"{group_name_clean}-group"
    tabs_id = f"{group_name_clean}-tabs"

    return (
        div(
            NAV_GROUP
            | {
                "id": group_id,
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
            key=group_id,
        ),
        div(
            TABS_COLLAPSE
            | {
                "id": tabs_id,
            },
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
            key=tabs_id,
        ),
    )
