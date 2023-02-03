import asyncio
import random
from typing import Sequence

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
    apps: Sequence[AppPackage],
):
    opacity, set_opacity = hooks.use_state(0)
    card_list = [card(app, key=app.uuid) for app in apps]
    min_show_len = 3
    show_more, set_show_more = hooks.use_state(len(card_list) <= min_show_len)

    @hooks.use_effect(dependencies=[])
    async def fade_in_animation():
        await asyncio.sleep(round(random.uniform(0, 0.3), 3))
        set_opacity(1)

    return div(
        div(
            div(
                h4(title, class_name="title"),
                p(description, class_name="description"),
                class_name="spotlight-title",
            ),
            [
                div(
                    button(
                        "Show More ",
                        i(class_name=f"fas fa-angle-{('up' if show_more else 'down')}"),
                        class_name="btn btn-sm btn-dark",
                        on_click=lambda _: set_show_more(not show_more),
                    ),
                    key="collapse-controls",
                    class_name="collapse-controls",
                )
            ]
            if len(card_list) > min_show_len
            else [],
            class_name="spotlight-head",
        ),
        div(
            div(card_list, class_name="collapse"),
            class_name=f"card-stage {('show-more' if show_more else '')}",
        ),
        class_name="spotlight-section fade-in",
        style={"opacity": opacity},
    )


def get_spotlight_categories():
    return SpotlightCategory.objects.all()
