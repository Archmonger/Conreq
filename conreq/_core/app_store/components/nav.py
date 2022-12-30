from typing import Iterable

from idom.html import a, div, h5, li, ol

from conreq._core.app_store.models import Category


def app_store_nav(categories: Iterable[Category]):
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
                                    "onClick": lambda x: print("clicked"),
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
