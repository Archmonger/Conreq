from copy import copy
from typing import Iterable, cast

from django_idom.components import django_css
from django_idom.hooks import use_query
from idom import component, hooks
from idom.html import _, div, h4, i, p
from idom.types import ComponentType

from conreq._core.app_store.components.card import card
from conreq._core.app_store.components.nav import app_store_nav
from conreq._core.app_store.models import AppPackage, Category, SpotlightCategory
from conreq.types import AppStoreState, AppStoreStateContext

# TODO: Handle situations where there are no spotlight apps or categories


@component
def app_store():  # sourcery skip
    state, set_state = hooks.use_state(AppStoreState())
    state.set_state = lambda obj: set_state(copy(obj))
    nav_category_query = use_query(get_nav_categories)

    if state.tab:
        print("current tab has been set!", state.tab.name)

    # Don't render if there's an error loading categories
    if nav_category_query.error:
        return "Error during loading apps!"

    # Don't render if there are no apps
    if not nav_category_query.loading and not nav_category_query.data:
        return "Error. No apps found!"

    # Don't render if categories are still loading
    if nav_category_query.loading:
        return None

    # TODO: Update app store entries every first load
    return AppStoreStateContext(
        django_css("conreq/app_store.css"),
        state.tab.name
        if state.tab
        else div(
            {"className": "spotlight-region"},
            all_spotlight(),
            key="spotlight-region",
        ),
        app_store_nav(nav_category_query.data),
        value=state,
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
    apps_query = use_query(get_spotlight_apps, apps)
    card_list, set_card_list = hooks.use_state(cast(list[ComponentType], []))

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
        {"className": "spotlight fade-in"},
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


def get_spotlight_apps(apps):
    return apps.all()


def get_spotlight_categories():
    return SpotlightCategory.objects.all()


def get_nav_categories():
    return Category.objects.all().order_by("order")
