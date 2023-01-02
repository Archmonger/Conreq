from copy import copy

from django_idom.components import django_css
from django_idom.hooks import use_query
from idom import component, hooks
from idom.html import _, div

from conreq._core.app_store.components.nav import app_store_nav
from conreq._core.app_store.components.spotlight import spotlight
from conreq._core.app_store.models import Category
from conreq.types import AppStoreState


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
    return _(
        django_css("conreq/app_store.css"),
        state.tab.name if state.tab else div({"className": "spotlight"}, spotlight()),
        app_store_nav(nav_category_query.data),
    )


def get_nav_categories():
    return Category.objects.all().order_by("order")
