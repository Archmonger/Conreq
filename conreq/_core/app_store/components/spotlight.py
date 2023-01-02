import asyncio
import random
from typing import Iterable

from django_idom.hooks import use_query
from idom import component, hooks
from idom.html import _, button, div, h4, i, p

from conreq._core.app_store.components.card import card
from conreq._core.app_store.models import AppPackage, SpotlightCategory


@component
def spotlight():
    spotlight_category_query = use_query(get_spotlight_categories)

    if spotlight_category_query.loading or spotlight_category_query.error:
        return

    return _(
        [
            spotlight_section(
                category.name,
                category.description,
                apps=category.apps.all(),
                key=category.uuid,
            )
            for category in spotlight_category_query.data  # type: ignore
        ]
    )


@component
def spotlight_section(
    title,
    description,
    apps: Iterable[AppPackage],
):
    opacity, set_opacity = hooks.use_state(0)
    show_more, set_show_more = hooks.use_state(False)
    card_list = [card(app, key=app.uuid) for app in apps]

    @hooks.use_effect(dependencies=[])
    async def fade_in_animation():
        await asyncio.sleep(round(random.uniform(0, 0.3), 3))
        set_opacity(1)

    return div(
        {
            "className": "spotlight-section fade-in",
            "style": {"opacity": opacity},
        },
        div(
            {"className": "spotlight-head"},
            div(
                {"className": "spotlight-title"},
                h4({"className": "title"}, title),
                p({"className": "description"}, description),
            ),
            div(
                {"className": "collapse-controls"},
                button(
                    {
                        "className": "btn btn-sm btn-dark",
                        "onClick": lambda _: set_show_more(not show_more),
                    },
                    "Show More ",
                    i({"className": f'fas fa-angle-{"up" if show_more else "down"}'}),
                ),
            ),
        ),
        div(
            {"className": "card-stage"}
            | ({"style": {"height": "auto"}} if show_more else {}),
            div(
                {"className": "collapse"}
                | (
                    {"style": {"flex-flow": "wrap", "width": "auto"}}
                    if show_more
                    else {}
                ),
                card_list,
            ),
        ),
    )


def get_spotlight_categories():
    return SpotlightCategory.objects.all()
