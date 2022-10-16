import asyncio
import random
from typing import Callable, Iterable

from django_idom.components import django_css
from django_idom.hooks import use_query
from idom import component, hooks
from idom.html import _, a, div, h4, p

from conreq._core.app_store.components.card import card
from conreq._core.app_store.components.nav import app_store_nav
from conreq._core.app_store.models import AppPackage, SpotlightCategory, Subcategory
from conreq.types import HomepageState

# pylint: disable=unused-argument
# TODO: Handle situations where there are no spotlight apps or categories


@component
def app_store(state: HomepageState, set_state: Callable[[HomepageState], None]):
    # pylint: disable=unused-argument,protected-access
    tab, set_tab = hooks.use_state(None)
    nav_category_query = use_query(get_nav_categories)
    nav_categories, set_nav_categories = hooks.use_state({})
    loading_needed, set_loading_needed = hooks.use_state(True)

    # Display loading animation until categories are loaded
    if loading_needed and not nav_categories:
        state.viewport_loading = True
        set_loading_needed(False)
        set_state(state)

    # Hide loading animation once categories are loaded
    if not loading_needed and nav_categories:
        state.viewport_loading = False
        set_loading_needed(True)
        set_state(state)

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
            _(all_spotlight(state, set_state, set_tab)),
            key="spotlight-region",
        ),
        div({"className": "nav-region blur"}, app_store_nav(nav_categories, set_tab)),
    )


@component
def all_spotlight(
    state: HomepageState, set_state: Callable[[HomepageState], None], set_tab
):
    spotlight_category_query = use_query(get_spotlight_categories)

    if spotlight_category_query.loading or spotlight_category_query.error:
        return

    query_data: Iterable[SpotlightCategory] = spotlight_category_query.data  # type: ignore

    return _(
        [
            spotlight(
                category.name,
                category.description,
                state,
                set_state,
                set_tab,
                apps=category.apps,
                key=category.uuid,
            )
            for category in query_data
        ]
    )


@component
def spotlight(
    title,
    description,
    state: HomepageState,
    set_state: Callable[[HomepageState], None],
    set_tab,
    apps: Iterable[AppPackage],
    special=False,
):
    opacity, set_opacity = hooks.use_state(0)
    apps_query = use_query(get_spotlight_apps, apps)

    @hooks.use_effect(dependencies=[])
    async def fade_in_animation():
        await asyncio.sleep(round(random.uniform(0, 0.3), 3))
        set_opacity(1)

    if apps_query.loading or apps_query.error:
        return

    query_data: Iterable[AppPackage] = apps_query.data  # type: ignore

    return div(
        {
            "className": "spotlight fade-in",
            "style": {"opacity": opacity},
        },
        a(
            {"href": "#", "onClick": lambda x: print("clicked")},
            h4({"className": "title"}, title),
            p({"className": "description"}, description),
        ),
        div(
            {"className": "card-stage"},
            _(
                [
                    card(state, set_state, set_tab, special, app, key=app.uuid)
                    for app in query_data
                ]
            ),
        ),
    )


def get_spotlight_apps(apps):
    return apps.all()


def get_spotlight_categories():
    return SpotlightCategory.objects.all()


def get_nav_categories():
    return Subcategory.objects.select_related("category").order_by("name").all()


def subcategories_to_dict(query) -> dict[str, dict[str, str]]:
    new_categories = {}
    for subcategory in query:
        new_categories.setdefault(subcategory.category, []).append(subcategory)
    return new_categories
