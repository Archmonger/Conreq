from copy import copy
from typing import Callable, Optional

import idom
from django.contrib import auth
from django.shortcuts import render
from idom.html import div, li, ul

from conreq import AuthLevel, HomepageState, TabbedViewportState
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
    tabs: dict,
    top_tabs: Optional[dict] = None,
    bottom_tabs: Optional[dict] = None,
    default_tab: Optional[Callable] = None,
):
    """Generates a viewport with the provided tabs. Viewport functions should accept
    `websocket, state, set_state` as arguements."""
    tab_state, set_tab_state = idom.hooks.use_state(
        TabbedViewportState(
            _default_tab(top_tabs, tabs, bottom_tabs, default_tab=default_tab)
        )
    )

    return div(
        {"className": "tabbed-viewport-container"},
        div(
            {"className": "tabbed-viewport"},
            tab_state.current_tab(websocket, state, set_state),
        ),
        ul(
            {"className": "tabbed-viewport-selector list-group"},
            *_tabbed_viewport_tabs(top_tabs, tab_state, set_tab_state),
            *_tabbed_viewport_tabs(tabs, tab_state, set_tab_state),
            *_tabbed_viewport_tabs(bottom_tabs, tab_state, set_tab_state),
        ),
    )


def _default_tab(*tab_groups, default_tab=None):
    if default_tab:
        return default_tab

    for tabs in tab_groups:
        if tabs:
            return tabs[next(iter(tabs))]["component"]

    return None


def _tabbed_viewport_tabs(tabs: dict, tab_state: TabbedViewportState, set_tab_state):
    if not tabs:
        return []

    return [
        li(
            _tabbed_viewport_tabs_values(tab_properties, tab_state, set_tab_state),
            tab_name,
        )
        for tab_name, tab_properties in tabs.items()
    ]


def _tabbed_viewport_tabs_values(
    tab_properties, tab_state: TabbedViewportState, set_tab_state
):
    async def on_click(_):
        tab_state.current_tab = tab_properties["component"]
        set_tab_state(copy(tab_state))

    return {
        "className": f"list-group-item clickable{' active' if tab_state.current_tab is tab_properties['component'] else ''}",
        "onClick": on_click,
    }
