from idom.html import a, div, h5, li, ol

from conreq._core.app_store.models import Category, Subcategory

# pylint: disable=unused-argument


def app_store_nav(categories: dict[Category, list[Subcategory]], set_tab):
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
                        for subcategory in value
                    ],
                ),
                key=str(category.uuid),
            )
            for category, value in categories.items()
        ],
    )
