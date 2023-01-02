import asyncio
import random
from copy import copy
from typing import Iterable

from django_idom.hooks import use_query
from idom import component, hooks
from idom.html import _, div, h4, i, p

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
    card_list, set_card_list = hooks.use_state(
        [card(app, key=app.uuid) for app in apps]
    )

    @hooks.use_effect(dependencies=[])
    async def fade_in_animation():
        await asyncio.sleep(round(random.uniform(0, 0.3), 3))
        set_opacity(1)

    def rotate_left(_):
        set_card_list(copy(card_list[-1:] + card_list[:-1]))

    def rotate_right(_):
        card_list.append(card_list.pop(0))
        set_card_list(copy(card_list))

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
                {"className": "carousel-controls"},
                i({"className": "fas fa-angle-left", "onClick": rotate_left}),
                i({"className": "fas fa-angle-right", "onClick": rotate_right}),
            ),
        ),
        div(
            {"className": "card-stage"},
            div(
                {"className": "carousel"},
                card_list,
            ),
        ),
    )


def get_spotlight_categories():
    return SpotlightCategory.objects.all()
