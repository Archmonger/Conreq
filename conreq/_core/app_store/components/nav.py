from typing import Sequence

from idom import hooks
from idom.html import a, div, h5, li, ol

from conreq._core.app_store.models import Category
from conreq.types import AppStoreStateContext


def app_store_nav(categories: Sequence[Category]):
    state = hooks.use_context(AppStoreStateContext)

    def nav_onclick(subcategory):
        def event(_):
            state.tab = subcategory
            state.set_state(state)

        return event

    return div(
        {"class_name": "nav-region"},
        [
            div(
                {"class_name": "nav-item", "key": str(category.uuid)},
                h5({"class_name": "nav-title"}, category.name),
                ol(
                    {"class_name": "nav-sub"},
                    [
                        li(
                            {
                                "class_name": "nav-sub-item",
                                "key": str(subcategory.uuid),
                            },
                            a(
                                {
                                    "class_name": "nav-sub-link",
                                    "href": f"#{subcategory.uuid}",
                                    "on_click": nav_onclick(subcategory),
                                },
                                subcategory.name,
                            ),
                        )
                        for subcategory in sorted(
                            category.subcategory_set.all(), key=lambda x: x.name
                        )
                    ],
                ),
            )
            for category in categories
        ],
    )
