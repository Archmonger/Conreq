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
        [
            div(
                h5(category.name, class_name="nav-title"),
                ol(
                    [
                        li(
                            a(
                                subcategory.name,
                                class_name="nav-sub-link",
                                href=f"#{subcategory.uuid}",
                                on_click=nav_onclick(subcategory),
                            ),
                            key=str(subcategory.uuid),
                            class_name="nav-sub-item",
                        )
                        for subcategory in sorted(
                            category.subcategory_set.all(), key=lambda x: x.name
                        )
                    ],
                    class_name="nav-sub",
                ),
                key=str(category.uuid),
                class_name="nav-item",
            )
            for category in categories
        ],
        class_name="nav-region",
    )
