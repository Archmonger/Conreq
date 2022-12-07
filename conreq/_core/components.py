from copy import copy
from inspect import iscoroutinefunction
from uuid import uuid4

from django_idom.hooks import use_websocket
from idom import component, hooks
from idom.html import div, li, ul

from conreq.types import (
    HomepageState,
    HomepageStateContext,
    SubTab,
    SubTabEvent,
    TabbedViewportState,
    TabbedViewportStateContext,
)


@component
def tabbed_viewport(
    tabs: list[SubTab],
    top_tabs: list[SubTab] | None = None,
    bottom_tabs: list[SubTab] | None = None,
    default_tab: SubTab | None = None,
):
    """Generates a viewport with the provided tabs."""
    tab_state, _set_tab_state = hooks.use_state(
        TabbedViewportState(
            _default_tab(
                top_tabs or [], tabs, bottom_tabs or [], default_tab=default_tab
            )
        )
    )

    def _set_tab_state_copy(obj):
        new_obj = copy(obj)
        _set_tab_state(new_obj)

    tab_state.set_state = _set_tab_state_copy

    if not tab_state or not tab_state.tab:
        return

    html_class = tab_state.tab.html_class

    return TabbedViewportStateContext(
        div(
            {
                "className": "tabbed-viewport-container"
                + (f" {html_class}" if html_class else "")
            },
            div(
                {"className": "tabbed-viewport"},
                tab_state.tab.component(),
            ),
            ul(
                {"className": "tabbed-viewport-selector list-group"},
                _subtabs(top_tabs),
                _subtabs(tabs),
                _subtabs(bottom_tabs),
            ),
        ),
        value=tab_state,
    )


def _default_tab(
    *tab_groups: list[SubTab], default_tab: SubTab | None = None
) -> SubTab | None:
    return default_tab or next((tabs[0] for tabs in tab_groups if tabs), None)


@component
def _subtabs(
    tabs: list[SubTab] | None,
):
    # sourcery skip: assign-if-exp
    state = hooks.use_context(HomepageStateContext)
    tab_state = hooks.use_context(TabbedViewportStateContext)
    websocket = use_websocket()

    if not tabs:
        return None

    return [
        li(
            _subtab_attributes(state, tab_state, tab, websocket),
            tab.name,
            key=str(uuid4()),
        )
        for tab in tabs
    ]


def _subtab_attributes(
    state: HomepageState,
    tab_state: TabbedViewportState,
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
                tabbed_viewport_state=tab_state,
            )
            if iscoroutinefunction(tab.on_click):
                await tab.on_click(click_event)
            else:
                tab.on_click(click_event)
            return

        tab_state.tab = tab
        tab_state.set_state(tab_state)

    return {
        "className": f"list-group-item clickable{' active' if tab_state.tab is tab else ''}",
        "onClick": on_click,
    }
