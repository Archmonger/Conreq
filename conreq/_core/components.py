from copy import copy
from inspect import iscoroutinefunction
from uuid import uuid4

import idom
from django_idom.hooks import use_websocket
from idom.core.types import VdomDict
from idom.html import div, li, ul

from conreq.types import HomepageState, SubTab, SubTabEvent, TabbedViewportState


@idom.component
def tabbed_viewport(
    state: HomepageState,
    set_state,
    tabs: list[SubTab],
    top_tabs: list[SubTab] | None = None,
    bottom_tabs: list[SubTab] | None = None,
    default_tab: SubTab | None = None,
):
    """Generates a viewport with the provided tabs. Viewport functions should accept
    `state, set_state` as arguements."""
    tab_state, _set_tab_state = idom.hooks.use_state(
        TabbedViewportState(
            _default_tab(
                top_tabs or [], tabs, bottom_tabs or [], default_tab=default_tab
            )
        )
    )

    def set_tab_state(obj):
        new_obj = copy(obj)
        _set_tab_state(new_obj)

    websocket = use_websocket()

    if not tab_state or not tab_state.current_tab:
        return

    html_class = tab_state.current_tab.html_class

    return div(
        {
            "className": "tabbed-viewport-container"
            + (f" {html_class}" if html_class else "")
        },
        div(
            {"className": "tabbed-viewport"},
            tab_state.current_tab.component(state, set_state),
        ),
        ul(
            {"className": "tabbed-viewport-selector list-group"},
            _subtabs(state, set_state, tab_state, set_tab_state, top_tabs, websocket),
            _subtabs(state, set_state, tab_state, set_tab_state, tabs, websocket),
            _subtabs(
                state, set_state, tab_state, set_tab_state, bottom_tabs, websocket
            ),
        ),
    )


def _default_tab(
    *tab_groups: list[SubTab], default_tab: SubTab | None = None
) -> SubTab | None:
    return default_tab or next((tabs[0] for tabs in tab_groups if tabs), None)


def _subtabs(
    state: HomepageState,
    set_state,
    tab_state: TabbedViewportState,
    set_tab_state,
    tabs: list[SubTab] | None,
    websocket,
) -> list[VdomDict]:
    # sourcery skip: assign-if-exp
    if not tabs:
        return []

    return [
        li(
            _subtab_attributes(
                state, set_state, tab_state, set_tab_state, tab, websocket
            ),
            tab.name,
            key=str(uuid4()),
        )
        for tab in tabs
    ]


def _subtab_attributes(
    state: HomepageState,
    set_state,
    tab_state: TabbedViewportState,
    set_tab_state,
    tab: SubTab,
    websocket,
) -> dict:
    async def on_click(event):
        if tab.on_click:
            click_event = SubTabEvent(
                event=event,
                tab=tab,
                websocket=websocket,
                homepage_state=state,
                set_homepage_state=set_state,
                tabbed_viewport_state=tab_state,
                set_tabbed_viewport_state=set_tab_state,
            )
            if iscoroutinefunction(tab.on_click):
                await tab.on_click(click_event)
            else:
                tab.on_click(click_event)
            return

        tab_state.current_tab = tab
        set_tab_state(tab_state)

    return {
        "className": f"list-group-item clickable{' active' if tab_state.current_tab is tab else ''}",
        "onClick": on_click,
    }
