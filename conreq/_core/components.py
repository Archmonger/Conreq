from copy import copy
from inspect import iscoroutinefunction
from typing import Callable
from uuid import uuid4

import idom
from idom.core.types import VdomDict
from idom.html import div, li, ul

from conreq.types import HomepageState, Tab, TabbedViewportState


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
            _tabbed_viewport_tabs(
                websocket, state, set_state, tab_state, set_tab_state, top_tabs
            ),
            _tabbed_viewport_tabs(
                websocket, state, set_state, tab_state, set_tab_state, tabs
            ),
            _tabbed_viewport_tabs(
                websocket, state, set_state, tab_state, set_tab_state, bottom_tabs
            ),
        ),
    )


def _default_tab(*tab_groups: list[Tab], default_tab: Callable = None) -> Tab:
    return default_tab or next((tabs[0] for tabs in tab_groups if tabs), None)


def _tabbed_viewport_tabs(
    websocket,
    state: HomepageState,
    set_state,
    tab_state: TabbedViewportState,
    set_tab_state,
    tabs: list[Tab],
) -> list[VdomDict]:
    # sourcery skip: assign-if-exp
    if not tabs:
        return []

    return [
        li(
            _tabbed_viewport_tabs_values(
                websocket, state, set_state, tab_state, set_tab_state, tab
            ),
            tab.name,
            key=str(uuid4()),
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
            if iscoroutinefunction(tab.on_click):
                await tab.on_click(
                    event,
                    state=state,
                    set_state=set_state,
                    websocket=websocket,
                    tab_state=tab_state,
                    set_tab_state=set_tab_state,
                    tab=tab,
                )
            else:
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
