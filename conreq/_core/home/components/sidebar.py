from copy import copy
from inspect import iscoroutinefunction

import idom
from idom.html import _, div, i, nav

from conreq import HomepageState, NavGroup, NavTab, Viewport, ViewportSelector, config
from conreq.utils.environment import get_debug_mode, get_safe_mode
from conreq.utils.generic import clean_string

# pylint: disable=protected-access

DEBUG = get_debug_mode()
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

    nav_tabs = config.homepage.nav_tabs

    @idom.hooks.use_effect
    async def set_initial_tab():
        # The initial tab has already been set
        if state._viewport_selector != ViewportSelector._initial:
            return None

        # Use the configured default tab, if it exists
        if config.homepage.default_nav_tab:
            state._viewport_selector = config.homepage.default_nav_tab.viewport.selector
            state._viewport_primary = config.homepage.default_nav_tab.viewport
            set_state(copy(state))
            return None

        # Select the top most tab, if it exists
        for group in nav_tabs:
            if not group.tabs or group in USER_ADMIN_DEBUG:
                continue
            tab: NavTab = group.tabs[0]
            state._viewport_selector = tab.viewport.selector
            if tab["viewport"] == ViewportSelector.primary:
                state._viewport_primary = tab.viewport
            if tab.viewport.selector == ViewportSelector.secondary:
                state._viewport_secondary = tab.viewport
            set_state(copy(state))
            return None

    async def username_on_click(_):
        state._viewport_selector = ViewportSelector.primary
        state._viewport_primary = Viewport(config.components.user_settings)
        set_state(copy(state))

    return nav(
        SIDEBAR,
        SIDEBAR_SAFE_MODE if SAFE_MODE else "",
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
            [  # App tabs
                nav_group(websocket, state, set_state, group)
                for group in nav_tabs
                if group not in USER_ADMIN_DEBUG
            ],
            [  # User tabs
                nav_group(
                    websocket,
                    state,
                    set_state,
                    group,
                    bottom_tabs=config._homepage.user_nav_tabs,
                )
                for group in nav_tabs
                if group == "User"
            ],
            [  # Admin tabs
                nav_group(
                    websocket,
                    state,
                    set_state,
                    group,
                    bottom_tabs=config._homepage.admin_nav_tabs,
                )
                for group in nav_tabs
                if group == "Admin" and websocket.scope["user"].is_staff
            ],
            [  # Debug tabs
                nav_group(
                    websocket,
                    state,
                    set_state,
                    group,
                    top_tabs=config._homepage.debug_nav_tabs,
                )
                for group in nav_tabs
                if group == "Debug" and websocket.scope["user"].is_staff and DEBUG
            ],
        ),
    )


def nav_tab_class(state: HomepageState, tab: NavTab):
    if (
        state._viewport_selector
        not in {
            ViewportSelector._loading,
            ViewportSelector._initial,
        }
        and tab.viewport.component
        is state.__getattribute__(f"_viewport_{state._viewport_selector}").component
    ):
        return NAV_TAB_ACTIVE
    return NAV_TAB


def nav_tab(websocket, state: HomepageState, set_state, tab: NavTab):
    async def on_click(event):
        if tab.on_click:
            if iscoroutinefunction(tab.on_click):
                await tab.on_click(
                    event,
                    websocket=websocket,
                    state=state,
                    set_state=set_state,
                    tab=tab,
                )
            else:
                tab.on_click(
                    event,
                    websocket=websocket,
                    state=state,
                    set_state=set_state,
                    tab=tab,
                )
            return
        state.set_viewport(tab.viewport)
        set_state(copy(state))

    return div(
        nav_tab_class(state, tab) | {"onClick": on_click},
        div(TAB_NAME, tab.name),
        key=tab.name,
    )


def nav_group(
    websocket,
    state: HomepageState,
    set_state,
    group: NavGroup,
    top_tabs: list[NavTab] = None,
    bottom_tabs: list[NavTab] = None,
):
    _top_tabs = top_tabs or []
    _bottom_tabs = bottom_tabs or []
    group_name_clean = clean_string(group.name, lowercase=False)
    group_id = f"{group_name_clean}-group"
    tabs_id = f"{group_name_clean}-tabs"

    return _(
        div(
            NAV_GROUP
            | {
                "id": group_id,
                "data-bs-target": f"#{tabs_id}",
                "aria-controls": tabs_id,
                "title": group.name,
            },
            div(
                GROUP_NAME,
                div(GROUP_ICON, group.icon or DEFAULT_NAV_GROUP_ICON),
                group.name,
            ),
            i(GROUP_CARET | {"title": f'Collapse the "{group.name}" group.'}),
        ),
        div(
            TABS_COLLAPSE
            | {
                "id": tabs_id,
            },
            div(TABS_INDICATOR),
            div(
                TABS,
                [nav_tab(websocket, state, set_state, tab) for tab in _top_tabs],
                [nav_tab(websocket, state, set_state, tab) for tab in group.tabs],
                [nav_tab(websocket, state, set_state, tab) for tab in _bottom_tabs],
            ),
        ),
        key=group_id,
    )
