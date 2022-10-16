import asyncio
import random
from typing import Callable

from idom import component, hooks
from idom.html import a, button, div, h5

from conreq._core.app_store.models import AppPackage
from conreq.types import HomepageState

# pylint: disable=unused-argument


@component
def card(
    state: HomepageState,
    set_state: Callable[[HomepageState], None],
    set_tab,
    special,
    app: AppPackage,
):
    opacity, set_opacity = hooks.use_state(0)

    def click_details_btn(_):
        state.modal_state.show = True
        set_state(state)

    @hooks.use_effect(dependencies=[])
    async def fade_in_animation():
        await asyncio.sleep(round(random.uniform(0, 0.55), 3))
        set_opacity(1)

    return div(
        {
            "className": "card fade-in" + (" special" if special else ""),
            "style": {"opacity": opacity},
        },
        div(
            {"className": "top"},
            div(
                {"className": "text-region"},
                h5(
                    {"className": "card-title"},
                    a(
                        {"href": f"#{app.uuid}", "onClick": lambda x: print("clicked")},
                        app.name,
                    ),
                ),
                div(
                    {"className": "card-author"},
                    a(
                        {"href": "#", "onClick": lambda x: print("clicked")},
                        app.author,
                    ),
                ),
            ),
            div({"className": "image"}),
        ),
        div(
            {"className": "btn-container"},
            button(
                {
                    "className": "btn btn-sm btn-secondary",
                    "onClick": click_details_btn,
                },
                "Details",
            ),
            button(
                {
                    "className": "btn btn-sm btn-primary",
                    "onClick": lambda x: print("clicked"),
                },
                "Install",
            ),
        ),
        div({"className": "description"}, app.short_description),
    )
