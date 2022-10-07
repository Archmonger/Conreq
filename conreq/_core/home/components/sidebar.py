from inspect import iscoroutinefunction

import idom
from django_idom.hooks import use_websocket
from idom.html import _, div, i, nav

from conreq import HomepageState, NavGroup, SidebarTab, Viewport, config
from conreq._core.home.components.welcome import welcome
from conreq.types import SidebarTabEvent
from conreq.utils.environment import get_debug_mode, get_safe_mode
from conreq.utils.generic import clean_string

# pylint: disable=protected-access

DEBUG = get_debug_mode()
SAFE_MODE = get_safe_mode()
SIDEBAR = {"id": "sidebar", "className": "sidebar no-hightlighting blur collapsed"}
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
def sidebar(state: HomepageState, set_state):
    websocket = use_websocket()
    if not websocket.scope["user"].is_authenticated:
        return None

    sidebar_tabs = config.homepage.sidebar_tabs

    @idom.hooks.use_effect(dependencies=[])
    async def set_initial_tab():
        # The initial tab has already been set
        if state._viewport or state._viewport_intent:
            return None

        # Use the configured default tab, if it exists
        if config.homepage.default_sidebar_tab:
            state._viewport_intent = config.homepage.default_sidebar_tab.viewport
            set_state(state)
            return None

        # Select the top most tab, if it exists
        for group in sidebar_tabs:
            if not group.tabs or group in USER_ADMIN_DEBUG:
                continue
            tab: SidebarTab = group.tabs[0]
            state._viewport_intent = tab.viewport
            set_state(state)
            return None

        # Tell the user to install some apps, if they don't have any
        state._viewport_intent = Viewport(welcome)
        set_state(state)

    async def username_on_click(_):
        if not config.tabs.user_settings.main:
            return
        state._viewport_intent = config.tabs.user_settings.main.viewport
        set_state(state)

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
            NAVIGATION,  # TODO: Change these keys to be database IDs
            [  # App tabs
                sidebar_group(
                    state,
                    set_state,
                    group,
                    key=group.name,
                )
                for group in sidebar_tabs
                if group not in USER_ADMIN_DEBUG
            ],  # type: ignore
            [  # User tabs
                sidebar_group(
                    state,
                    set_state,
                    group,
                    bottom_tabs=config._homepage.user_sidebar_tabs,
                    key=group.name,
                )
                for group in sidebar_tabs
                if group == "User"
            ],  # type: ignore
            [  # Admin tabs
                sidebar_group(
                    state,
                    set_state,
                    group,
                    bottom_tabs=config._homepage.admin_sidebar_tabs,
                    key=group.name,
                )
                for group in sidebar_tabs
                if group == "Admin" and websocket.scope["user"].is_staff
            ],  # type: ignore
            [  # Debug tabs
                sidebar_group(
                    state,
                    set_state,
                    group,
                    top_tabs=config._homepage.debug_sidebar_tabs,
                    key=group.name,
                )
                for group in sidebar_tabs
                if group == "Debug" and websocket.scope["user"].is_staff and DEBUG
            ],  # type: ignore
        ),
    )


def _sidebar_tab_class(state: HomepageState, tab: SidebarTab):
    if state._viewport and getattr(tab.viewport, "component", None) is getattr(
        state._viewport, "component", None
    ):
        return NAV_TAB_ACTIVE
    return NAV_TAB


@idom.component
def sidebar_tab(state: HomepageState, set_state, tab: SidebarTab):
    websocket = use_websocket()

    async def on_click(event):
        if tab.on_click:
            click_event = SidebarTabEvent(
                event=event,
                tab=tab,
                websocket=websocket,
                homepage_state=state,
                set_homepage_state=set_state,
            )
            if iscoroutinefunction(tab.on_click):
                await tab.on_click(click_event)
            else:
                tab.on_click(click_event)
            return

        # Don't reload if clicking the current tab
        if getattr(tab.viewport, "component", None) is getattr(
            state._viewport, "component", None
        ):
            return

        # Switch tabs
        if tab.viewport:
            # Reset loading state (only set by user defined viewports)
            state._viewport_loading = False

            state.set_viewport(tab.viewport)
            set_state(state)

    return div(
        _sidebar_tab_class(state, tab) | {"onClick": on_click},
        div(TAB_NAME, tab.name),
        key=tab.name,
    )


@idom.component
def sidebar_group(
    state: HomepageState,
    set_state,
    group: NavGroup,
    top_tabs: list[SidebarTab] | None = None,
    bottom_tabs: list[SidebarTab] | None = None,
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
                TABS,  # TODO: Change these keys to be database IDs
                [sidebar_tab(state, set_state, tab, key=tab.name) for tab in _top_tabs],  # type: ignore
                [
                    sidebar_tab(state, set_state, tab, key=tab.name)
                    for tab in group.tabs
                ],  # type: ignore
                [
                    sidebar_tab(state, set_state, tab, key=tab.name)
                    for tab in _bottom_tabs
                ],  # type: ignore
            ),
        ),
        key=group_id,
    )
