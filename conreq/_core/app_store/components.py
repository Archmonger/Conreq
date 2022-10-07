import asyncio
import random

from django_idom.components import django_css
from django_idom.hooks import use_query
from idom import component, hooks
from idom.html import _, a, button, div, h4, h5, li, ol, p

from conreq._core.app_store.models import Category, Subcategory
from conreq.types import HomepageState


class PlaceholderApp:
    uuid = 0
    name = "My App Name"
    short_description = "This is a placeholder description. This will be removed in the future. Please pay no attention to this text. But what if the text gets too long? Who knows what will happen, but I can probably guess that it'll be great! Or maybe it won't be, only time will tell."
    author = "Author"
    version = "0.0.0"
    category = "Category"


def subcategories_to_dict(query) -> dict[str, dict[str, str]]:
    new_categories = {}
    for subcategory in query:
        new_categories.setdefault(subcategory.category, []).append(subcategory)
    return new_categories


def get_categories():
    return Subcategory.objects.select_related("category").order_by("name").all()


@component
def app_store(state: HomepageState, set_state):
    # pylint: disable=unused-argument,protected-access
    tab, set_tab = hooks.use_state(None)
    category_query = use_query(get_categories)
    categories, set_categories = hooks.use_state({})
    loading_needed, set_loading_needed = hooks.use_state(True)

    # Display loading animation until categories are loaded
    if loading_needed and not categories:
        state.set_loading(True)
        set_loading_needed(False)
        set_state(state)

    # Hide loading animation once categories are loaded
    if not loading_needed and categories:
        state.set_loading(False)
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
                our_favorites(set_tab),
                most_popular(set_tab),
                recently_updated(set_tab),
                top_downloaded(set_tab),
                recently_added(set_tab),
                essentials(set_tab),
                random_selection(set_tab),
            ),
            key="spotlight-region",
        ),
        div({"className": "nav-region blur"}, app_store_nav(categories, set_tab)),
    )


def app_store_nav(categories: dict[Category, list[Subcategory]], set_tab) -> list:
    return [
        div(
            {"className": "nav-item"},
            a(
                {
                    "href": f"#{category.uuid}",
                    "onClick": lambda x: print("clicked"),
                },
                h5({"className": "nav-title"}, category.name),
            ),
            ol(
                {"className": "nav-sub"},
                [
                    li(
                        {"className": "nav-sub-item"},
                        a(
                            {
                                "className": "nav-sub-link",
                                "href": f"#{subcategory.uuid}",
                                "onClick": lambda x: print("clicked"),
                            },
                            subcategory.name,
                        ),
                        key=str(subcategory.uuid),
                    )
                    for subcategory in value
                ],
            ),
            key=str(category.uuid),
        )
        for category, value in categories.items()
    ]


@component
def recently_added(set_tab):
    return _(spotlight("Recently Added", "The latest from our community.", set_tab))


@component
def recently_updated(set_tab):
    return _(
        spotlight("Recently Updated", "Actively maintained for all to enjoy.", set_tab)
    )


@component
def most_popular(set_tab):
    return _(
        spotlight(
            "Most Popular", "These have gained a serious amount lot of love.", set_tab
        )
    )


@component
def top_downloaded(set_tab):
    return _(spotlight("Top Downloaded", "Tons of downloads!", set_tab))


@component
def our_favorites(set_tab):
    return _(
        spotlight(
            "Our Favorites", "A curated list of our favorites.", set_tab, special=True
        )
    )


@component
def essentials(set_tab):
    return _(
        spotlight(
            "Essentials", "Something we think all users should consider.", set_tab
        )
    )


@component
def random_selection(set_tab):
    return _(spotlight("Random Selection", "Are you feeling lucky today?", set_tab))


@component
def spotlight(title, description, set_tab, apps=None, special=False):
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
            _([card(set_tab, special, key=key) for key in range(8)]),
        ),
    )


@component
def card(set_tab, special, app: PlaceholderApp = PlaceholderApp()):
    opacity, set_opacity = hooks.use_state(0)

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
                div(
                    {"className": "card-category"},
                    a(
                        {"href": "#", "onClick": lambda x: print("clicked")},
                        app.category,
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
                    "onClick": lambda x: print("clicked"),
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
