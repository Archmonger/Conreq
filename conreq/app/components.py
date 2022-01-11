from copy import copy
from typing import Callable

import idom
from django.contrib import auth
from django.shortcuts import render
from idom.core.proto import VdomDict
from idom.html import div, li, ul

from conreq.app.types import AuthLevel, HomepageState, Tab, TabbedViewportState
from conreq.utils.components import view_to_component


@view_to_component(name="logout_parent_frame", auth_level=AuthLevel.anonymous)
def logout(request=None):
    """Logs a user out, then triggers a `reload-page` event on the current page."""
    auth.logout(request)
    return render(request, "conreq/refresh_parent_frame.html")


@view_to_component(name="refresh_parent_frame", auth_level=AuthLevel.anonymous)
def refresh(request=None):
    """Triggers a `reload-page` event on the current page."""
    logout(request)
    return render(request, "conreq/refresh_parent_frame.html")


@idom.component
def tabbed_viewport(
    websocket,
    state: HomepageState,
    set_state,
    tabs: list[Tab],
    top_tabs: list[Tab] = None,
    bottom_tabs: list[Tab] = None,
    default_tab: Tab = None,
) -> VdomDict:
    """Generates a viewport with the provided tabs. Viewport functions should accept
    `websocket, state, set_state` as arguements."""
    tab_state, set_tab_state = idom.hooks.use_state(
        TabbedViewportState(
            _default_tab(top_tabs, tabs, bottom_tabs, default_tab=default_tab)
        )
    )
    html_class = tab_state.current_tab.html_class

    return div(
        {
            "className": "tabbed-viewport-container"
            + (f" {html_class}" if html_class else "")
        },
        div(
            {"className": "tabbed-viewport"},
            tab_state.current_tab.component(websocket, state, set_state),
        ),
        ul(
            {"className": "tabbed-viewport-selector list-group"},
            *_tabbed_viewport_tabs(
                websocket, state, set_state, tab_state, set_tab_state, top_tabs
            ),
            *_tabbed_viewport_tabs(
                websocket, state, set_state, tab_state, set_tab_state, tabs
            ),
            *_tabbed_viewport_tabs(
                websocket, state, set_state, tab_state, set_tab_state, bottom_tabs
            ),
        ),
    )


def _default_tab(*tab_groups: list[Tab], default_tab: Callable = None) -> Tab:
    if default_tab:
        return default_tab

    for tabs in tab_groups:
        if tabs:
            return tabs[0]

    return None


def _tabbed_viewport_tabs(
    websocket,
    state: HomepageState,
    set_state,
    tab_state: TabbedViewportState,
    set_tab_state,
    tabs: list[Tab],
) -> list[VdomDict]:
    if not tabs:
        return []

    return [
        li(
            _tabbed_viewport_tabs_values(
                websocket, state, set_state, tab_state, set_tab_state, tab
            ),
            tab.name,
        )
        for tab in tabs
    ]


def _tabbed_viewport_tabs_values(
    websocket,
    state: HomepageState,
    set_state,
    tab_state: TabbedViewportState,
    set_tab_state,
    tab: Tab,
) -> dict:
    async def on_click(event):
        if tab.on_click:
            tab.on_click(
                event,
                state=state,
                set_state=set_state,
                websocket=websocket,
                tab_state=tab_state,
                set_tab_state=set_tab_state,
                tab=tab,
            )
            return

        tab_state.current_tab = tab
        set_tab_state(copy(tab_state))

    return {
        "className": f"list-group-item clickable{' active' if tab_state.current_tab is tab else ''}",
        "onClick": on_click,
    }
