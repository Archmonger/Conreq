from copy import copy

from reactpy import component, hooks
from reactpy_django.components import django_css
from reactpy_django.hooks import use_query

from conreq._core.app_store.components.nav import app_store_nav
from conreq._core.app_store.components.spotlight import spotlight
from conreq._core.app_store.models import Category
from conreq.types import AppStoreState, AppStoreStateContext


@component
def app_store():  # sourcery skip
    state, set_state = hooks.use_state(AppStoreState())
    state.set_state = lambda obj: set_state(copy(obj))
    nav_category_query = use_query(get_nav_categories)

    # Don't render if there's an error loading categories
    if nav_category_query.error:
        return "Error. Could not load apps!"

    # Don't render if there are no apps
    if not nav_category_query.loading and not nav_category_query.data:
        return "Error. No apps found!"

    # Don't render if categories are still loading
    if nav_category_query.loading:
        return None

    # TODO: Update app store entries every first load
    return AppStoreStateContext(
        django_css("conreq/app_store.css"),
        app_store_nav(nav_category_query.data),
        state.tab(
            *state.tab_args,
            *state.tab_kwargs,
            key=f"{state.tab.__module__}.{state.tab.__name__}",
        )
        if state.tab
        else spotlight(),
        value=state,
    )


def get_nav_categories():
    return Category.objects.all().order_by("order")
