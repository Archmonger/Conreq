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
        {"className": "nav-region"},
        [
            div(
                {"className": "nav-item"},
                h5({"className": "nav-title"}, category.name),
                ol(
                    {"className": "nav-sub"},
                    [
                        li(
                            {"className": "nav-sub-item"},
                            a(
                                {
                                    "className": "nav-sub-link",
                                    "href": f"#{subcategory.uuid}",
                                    "onClick": nav_onclick(subcategory),
                                },
                                subcategory.name,
                            ),
                            key=str(subcategory.uuid),
                        )
                        for subcategory in sorted(
                            category.subcategory_set.all(), key=lambda x: x.name
                        )
                    ],
                ),
                key=str(category.uuid),
            )
            for category in categories
        ],
    )
