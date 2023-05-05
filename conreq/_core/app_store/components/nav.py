from typing import Sequence

from reactpy import component, hooks
from reactpy.html import a, button, div, li, ul

from conreq._core.app_store.components.event import (
    category_click_event,
    subcategory_click_event,
)
from conreq._core.app_store.models import Category, Subcategory
from conreq.types import AppStoreStateContext


@component
def app_store_nav(categories: Sequence[Category]):
    state = hooks.use_context(AppStoreStateContext)

    async def return_click(_):
        state.tab = None
        state.set_state(state)

    return div(
        {"class_name": "nav-region"},
        div(
            {"class_name": "dropdown"},
            button(
                {
                    "class_name": "nav-btn btn btn btn-dark dropdown-toggle",
                    "type": "button",
                    "data-bs-toggle": "dropdown",
                    "aria-expanded": "false",
                },
                "Categories",
            ),
            ul(
                {"class_name": "dropdown-menu"},
                [dropdown_item(category, key=category.uuid) for category in categories],
            ),
        ),
        button({"class_name": "nav-btn btn btn btn-dark"}, "Manage Apps"),
        button(
            {"class_name": "nav-btn btn btn btn-dark return", "on_click": return_click},
            "Return",
        )
        if state.tab
        else "",
    )


@component
def dropdown_item(category: Category):
    state = hooks.use_context(AppStoreStateContext)

    return li(
        a(
            {
                "class_name": "dropdown-item",
                "href": f"#{category.uuid}",
                "on_click": category_click_event(state, category),
            },
            f"{category.name} »",
        ),
        ul(
            {"class_name": "dropdown-menu dropdown-submenu"},
            [
                dropdown_sub_item(
                    subcategory,
                    key=str(subcategory.uuid),
                )
                for subcategory in sorted(
                    category.subcategory_set.all(),
                    key=lambda x: x.name,
                )
            ],
        ),
    )


@component
def dropdown_sub_item(subcategory: Subcategory):
    state = hooks.use_context(AppStoreStateContext)

    return li(
        a(
            {
                "class_name": "dropdown-item",
                "href": f"#{subcategory.uuid}",
                "on_click": subcategory_click_event(state, subcategory),
            },
            subcategory.name,
        ),
    )
