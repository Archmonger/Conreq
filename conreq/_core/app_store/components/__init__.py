import asyncio
import random
from typing import Callable

from django_idom.components import django_css
from django_idom.hooks import use_query
from idom import component, hooks
from idom.html import _, a, div, h4, p

from conreq._core.app_store.components.card import card
from conreq._core.app_store.components.nav import app_store_nav
from conreq._core.app_store.models import Subcategory
from conreq.types import HomepageState

# pylint: disable=unused-argument


@component
def app_store(state: HomepageState, set_state: Callable[[HomepageState], None]):
    # pylint: disable=unused-argument,protected-access
    tab, set_tab = hooks.use_state(None)
    category_query = use_query(get_categories)
    categories, set_categories = hooks.use_state({})
    loading_needed, set_loading_needed = hooks.use_state(True)

    # Display loading animation until categories are loaded
    if loading_needed and not categories:
        state.viewport_loading = True
        set_loading_needed(False)
        set_state(state)

    # Hide loading animation once categories are loaded
    if not loading_needed and categories:
        state.viewport_loading = False
        set_loading_needed(True)
        set_state(state)

    # Convert categories to a dictionary for easier rendering
    if not category_query.loading and not category_query.error and not categories:
        set_categories(subcategories_to_dict(category_query.data))

    # Don't render if there's an error loading categories
    if category_query.error:
        return _("Error!")

    # Don't render if categories are still loading, or if they haven't been converted to a dict yet
    if category_query.loading or not categories:
        return None

    # TODO: Update app store entries every first load
    return _(
        django_css("conreq/app_store.css"),
        tab(key=tab.__name__)
        if tab
        else div(
            {"className": "spotlight-region"},
            _(
                most_popular(state, set_state, set_tab),
                recently_updated(state, set_state, set_tab),
                our_favorites(state, set_state, set_tab),
                top_downloaded(state, set_state, set_tab),
                recently_added(state, set_state, set_tab),
                essentials(state, set_state, set_tab),
                random_selection(state, set_state, set_tab),
            ),
            key="spotlight-region",
        ),
        div({"className": "nav-region blur"}, app_store_nav(categories, set_tab)),
    )


@component
def recently_added(
    state: HomepageState, set_state: Callable[[HomepageState], None], set_tab
):
    return _(
        spotlight(
            "Recently Added",
            "The latest from our community.",
            state,
            set_state,
            set_tab,
        )
    )


@component
def recently_updated(
    state: HomepageState, set_state: Callable[[HomepageState], None], set_tab
):
    return _(
        spotlight(
            "Recently Updated",
            "Actively maintained for all to enjoy.",
            state,
            set_state,
            set_tab,
        )
    )


@component
def most_popular(
    state: HomepageState, set_state: Callable[[HomepageState], None], set_tab
):
    return _(
        spotlight(
            "Most Popular",
            "These have gained a serious amount lot of love.",
            state,
            set_state,
            set_tab,
        )
    )


@component
def top_downloaded(
    state: HomepageState, set_state: Callable[[HomepageState], None], set_tab
):
    return _(
        spotlight("Top Downloaded", "Tons of downloads!", state, set_state, set_tab)
    )


@component
def our_favorites(
    state: HomepageState, set_state: Callable[[HomepageState], None], set_tab
):
    return _(
        spotlight(
            "Our Favorites",
            "A curated list of our favorites.",
            state,
            set_state,
            set_tab,
            special=True,
        )
    )


@component
def essentials(
    state: HomepageState, set_state: Callable[[HomepageState], None], set_tab
):
    return _(
        spotlight(
            "Essentials",
            "Something we think all users should consider.",
            state,
            set_state,
            set_tab,
        )
    )


@component
def random_selection(
    state: HomepageState, set_state: Callable[[HomepageState], None], set_tab
):
    return _(
        spotlight(
            "Random Selection",
            "Are you feeling lucky?",
            state,
            set_state,
            set_tab,
        )
    )


@component
def spotlight(
    title,
    description,
    state: HomepageState,
    set_state: Callable[[HomepageState], None],
    set_tab,
    apps=None,
    special=False,
):
    opacity, set_opacity = hooks.use_state(0)

    @hooks.use_effect(dependencies=[])
    async def fade_in_animation():
        await asyncio.sleep(round(random.uniform(0, 0.3), 3))
        set_opacity(1)

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
            _([card(state, set_state, set_tab, special, key=key) for key in range(8)]),
        ),
    )


def get_categories():
    return Subcategory.objects.select_related("category").order_by("name").all()


def subcategories_to_dict(query) -> dict[str, dict[str, str]]:
    new_categories = {}
    for subcategory in query:
        new_categories.setdefault(subcategory.category, []).append(subcategory)
    return new_categories
