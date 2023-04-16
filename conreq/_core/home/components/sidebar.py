from inspect import iscoroutinefunction

from reactpy import component, hooks
from reactpy.html import _, div, i, nav
from reactpy_django.hooks import use_connection, use_scope

from conreq import config
from conreq._core.home.components.welcome import welcome
from conreq.types import (
    HomepageState,
    HomepageStateContext,
    NavGroup,
    SidebarTab,
    SidebarTabEvent,
    Viewport,
)
from conreq.utils.environment import get_debug_mode, get_safe_mode
from conreq.utils.generic import clean_string

# pylint: disable=protected-access

DEBUG = get_debug_mode()
SAFE_MODE = get_safe_mode()
SIDEBAR = {"id": "sidebar", "class_name": "sidebar no-hightlighting blur collapsed"}
SIDEBAR_USER = {"class_name": "sidebar-user clickable"}
USER_PIC = {"class_name": "sidebar-profile-pic"}
USER_PIC_PLACEHOLDER = {"class_name": "fas fa-user"}
USERNAME_CONTAINER = {"class_name": "username-container"}
USERNAME = {"class_name": "username ellipsis"}
NAVIGATION = {"id": "navigation"}
NAV_GROUP = {
    "class_name": "nav-group clickable",
    "data-bs-toggle": "collapse",
    "aria-expanded": "true",
}
GROUP_NAME = {"class_name": "group-name ellipsis"}
GROUP_ICON = {"class_name": "group-icon"}
EXAMPLE_GROUP_ICON = {"class_name": "fas fa-user icon-left"}
GROUP_CARET = {"class_name": "fas fa-caret-up icon-right"}
TABS_COLLAPSE = {
    "class_name": "tabs-collapse collapse show",
}
TABS_INDICATOR = {"class_name": "tabs-indicator"}
TABS = {"class_name": "tabs"}
NAV_TAB = {"class_name": "nav-tab clickable"}
NAV_TAB_ACTIVE = {"class_name": "nav-tab clickable active"}
TAB_NAME = {"class_name": "tab-name ellipsis"}
DEFAULT_NAV_GROUP_ICON = i({"class_name": "far fa-circle"})
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
@component
def sidebar():
    state = hooks.use_context(HomepageStateContext)
    scope = use_scope()
    if not scope["user"].is_authenticated:
        return None

    sidebar_tabs = config.homepage.sidebar_tabs

    @hooks.use_effect(dependencies=[])
    async def set_initial_tab():
        # The initial tab has already been set
        if state._viewport or state.viewport_intent:
            return None

        # Use the configured default tab, if it exists
        if config.homepage.default_sidebar_tab:
            state.viewport_intent = config.homepage.default_sidebar_tab.viewport
            state.set_state(state)
            return None

        # Select the top most tab, if it exists
        for group in sidebar_tabs:
            if not group.tabs or group in USER_ADMIN_DEBUG:
                continue
            tab: SidebarTab = group.tabs[0]
            state.viewport_intent = tab.viewport
            state.set_state(state)
            return None

        # Tell the user to install some apps, if they don't have any
        state.viewport_intent = Viewport(welcome)
        state.set_state(state)

    async def username_on_click(_):
        if not config.tabs.user_settings.main:
            return
        state.viewport_intent = config.tabs.user_settings.main.viewport
        state.set_state(state)

    return nav(
        SIDEBAR,
        SIDEBAR_SAFE_MODE if SAFE_MODE else "",
        div(
            SIDEBAR_USER | {"on_click": username_on_click},
            div(USER_PIC, i(USER_PIC_PLACEHOLDER)),
            div(
                USERNAME_CONTAINER,
                div(USERNAME, scope["user"].get_username()),
            ),
        ),
        div(
            # pylint: disable=protected-access
            NAVIGATION,  # TODO: Change these keys to be database IDs
            [  # App tabs
                sidebar_group(group, key=group.name)
                for group in sidebar_tabs
                if group not in USER_ADMIN_DEBUG
            ],
            [  # User tabs
                sidebar_group(
                    group,
                    bottom_tabs=config._homepage.user_sidebar_tabs,
                    key=group.name,
                )
                for group in sidebar_tabs
                if group == "User"
            ],
            [  # Admin tabs
                sidebar_group(
                    group,
                    bottom_tabs=config._homepage.admin_sidebar_tabs,
                    key=group.name,
                )
                for group in sidebar_tabs
                if group == "Admin" and scope["user"].is_staff
            ],
            [  # Debug tabs
                sidebar_group(
                    group, top_tabs=config._homepage.debug_sidebar_tabs, key=group.name
                )
                for group in sidebar_tabs
                if group == "Debug" and scope["user"].is_staff and DEBUG
            ],
        ),
    )


def _sidebar_tab_class(state: HomepageState, tab: SidebarTab):
    if state._viewport and getattr(tab.viewport, "component", None) is getattr(
        state._viewport, "component", None
    ):
        return NAV_TAB_ACTIVE
    return NAV_TAB


@component
def sidebar_tab(tab: SidebarTab):
    state = hooks.use_context(HomepageStateContext)
    connection = use_connection()

    async def on_click(event):
        if tab.on_click:
            click_event = SidebarTabEvent(
                event=event,
                tab=tab,
                connection=connection,
                homepage_state=state,
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
            state.viewport_loading = False

            state.viewport_intent = tab.viewport
            state.set_state(state)

    return div(
        {"on_click": on_click, "key": tab.name} | _sidebar_tab_class(state, tab),
        div(TAB_NAME, tab.name),
    )


@component
def sidebar_group(
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
        {"key": group_id},
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
                [sidebar_tab(tab, key=tab.name) for tab in _top_tabs],
                [sidebar_tab(tab, key=tab.name) for tab in group.tabs],
                [sidebar_tab(tab, key=tab.name) for tab in _bottom_tabs],
            ),
        ),
    )
