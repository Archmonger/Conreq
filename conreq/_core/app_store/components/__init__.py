import asyncio
import random
from copy import copy
from typing import Callable, Iterable, Union, cast

from django_idom.components import django_css
from django_idom.hooks import use_query
from idom import component, hooks
from idom.html import _, div, h4, i, p
from idom.types import ComponentType

from conreq._core.app_store.components.card import card
from conreq._core.app_store.components.nav import app_store_nav
from conreq._core.app_store.models import (
    AppPackage,
    Category,
    SpotlightCategory,
    Subcategory,
)
from conreq.types import HomepageStateContext

# TODO: Handle situations where there are no spotlight apps or categories


@component
def app_store():
    state = hooks.use_context(HomepageStateContext)
    tab, set_tab = hooks.use_state(cast(Union[Callable, None], None))
    nav_category_query = use_query(get_nav_categories)
    nav_categories, set_nav_categories = hooks.use_state(
        cast(dict[Category, list[Subcategory]], {})
    )
    loading_needed, set_loading_needed = hooks.use_state(True)

    # Display loading animation until categories are loaded
    if loading_needed and not nav_categories:
        state.viewport_loading = True
        set_loading_needed(False)
        state.set_state(state)

    # Hide loading animation once categories are loaded
    if not loading_needed and nav_categories:
        state.viewport_loading = False
        set_loading_needed(True)
        state.set_state(state)

    # Convert categories to a dictionary for easier rendering
    if (
        not nav_category_query.loading
        and not nav_category_query.error
        and not nav_categories
    ):
        set_nav_categories(subcategories_to_dict(nav_category_query.data))

    # Don't render if there's an error loading categories
    if nav_category_query.error:
        return _("Error!")

    # Don't render if categories are still loading, or if they haven't been converted to a dict yet
    if nav_category_query.loading or not nav_categories:
        return None

    # TODO: Update app store entries every first load
    return _(
        django_css("conreq/app_store.css"),
        tab(key=tab.__name__)
        if tab
        else div(
            {"className": "spotlight-region"},
            _(all_spotlight()),
            key="spotlight-region",
        ),
        app_store_nav(nav_categories),
    )


@component
def all_spotlight():
    spotlight_category_query = use_query(get_spotlight_categories)

    if spotlight_category_query.loading or spotlight_category_query.error:
        return

    return _(
        [
            spotlight(
                category.name,
                category.description,
                apps=category.apps,
                key=category.uuid,
            )
            for category in spotlight_category_query.data  # type: ignore
        ]
    )


@component
def spotlight(
    title,
    description,
    apps: Iterable[AppPackage],
):
    opacity, set_opacity = hooks.use_state(0)
    apps_query = use_query(get_spotlight_apps, apps)
    card_list, set_card_list = hooks.use_state(cast(list[ComponentType], []))

    @hooks.use_effect(dependencies=[])
    async def fade_in_animation():
        await asyncio.sleep(round(random.uniform(0, 0.3), 3))
        set_opacity(1)

    if apps_query.loading or apps_query.error:
        return

    if not card_list:
        set_card_list(
            [card(app, key=app.uuid) for app in apps_query.data]  # type: ignore
        )
        return

    def rotate_left(_):
        set_card_list(copy(card_list[-1:] + card_list[:-1]))

    def rotate_right(_):
        card_list.append(card_list.pop(0))
        set_card_list(copy(card_list))

    return div(
        {
            "className": "spotlight fade-in",
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
                _(card_list),
            ),
        ),
    )


def get_spotlight_apps(apps):
    return apps.all()


def get_spotlight_categories():
    return SpotlightCategory.objects.all()


def get_nav_categories():
    return Subcategory.objects.select_related("category").order_by("name").all()


def subcategories_to_dict(query) -> dict[Category, list[Subcategory]]:
    new_categories: dict[Category, list[Subcategory]] = {}
    for subcategory in query:
        new_categories.setdefault(subcategory.category, []).append(subcategory)
    return new_categories
