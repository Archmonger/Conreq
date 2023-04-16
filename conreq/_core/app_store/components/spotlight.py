import asyncio
import random

from django.db.models.manager import Manager
from django_idom.hooks import use_query
from idom import component, hooks
from idom.html import _, div, h4, p
from idom.types import VdomChild

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
                apps=category.apps,
                key=category.uuid,
            )
            for category in spotlight_category_query.data  # type: ignore
        ]
    )


@component
def spotlight_section(
    title,
    description,
    apps: Manager[AppPackage],
):
    # FIXME: This shouldn't be needed, but `OrderedManyToManyField` doesn't work with `django_query_postprocessor`
    spotlight_apps_query = use_query(get_spotlight_apps, apps)
    opacity, set_opacity = hooks.use_state(0)
    card_list: list[VdomChild] = (
        [card(app, key=app.uuid) for app in spotlight_apps_query.data]  # type: ignore
        if spotlight_apps_query.data
        else []
    )

    @hooks.use_effect(dependencies=[])
    async def fade_in_animation():
        await asyncio.sleep(round(random.uniform(0, 0.3), 3))
        set_opacity(1)

    return div(
        {"class_name": "spotlight-section fade-in", "style": {"opacity": opacity}},
        div(
            {"class_name": "spotlight-head"},
            div(
                {"class_name": "spotlight-title"},
                h4({"class_name": "title"}, title),
                p({"class_name": "description"}, description),
            ),
        ),
        div(
            {"class_name": "card-stage show-more"},
            div({"class_name": "collapse"}, card_list),
        ),
    )


def get_spotlight_categories():
    return SpotlightCategory.objects.all()


def get_spotlight_apps(apps: Manager[AppPackage]):
    return apps.all()