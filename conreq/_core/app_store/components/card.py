import random

from django_idom.hooks import use_query
from django_idom.types import QueryOptions
from idom import component, hooks
from idom.html import a, button, div, h5

from conreq._core.app_store.models import AppPackage
from conreq.types import HomepageStateContext


def get_app_subcategory(app: AppPackage):
    return app.subcategories.first()


def check_installable(app: AppPackage):
    return app.installable


@component
def card(app: AppPackage):
    state = hooks.use_context(HomepageStateContext)
    animation_speed, _ = hooks.use_state(random.randint(7, 13))
    subcategory = use_query(get_app_subcategory, app)
    installable = use_query(QueryOptions(postprocessor=None), check_installable, app)

    def details_modal_event(_):
        state.modal_state.show = True
        state.set_state(state)

    return div(
        {
            "className": "card fade-in" + (" special" if app.special else ""),
            "style": {"--animation-speed": f"{animation_speed}s"}
            if app.special
            else {},
        },
        div(
            {"className": "top"},
            div(
                {"className": "text-region"},
                h5(
                    {"className": "card-title"},
                    a(
                        {"href": f"#{app.uuid}", "onClick": details_modal_event},
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
                        str(subcategory.data) if subcategory.data else "",
                    ),
                ),
            ),
            div({"className": "image"}),
        ),
        div(
            {"className": "btn-container"},
            button(
                {
                    "className": "btn btn-sm btn-dark",
                    "onClick": details_modal_event,
                },
                "Details",
            ),
            [
                a(
                    {
                        "href": f"mailto:{app.author_email}",
                        "className": "btn btn-sm btn-dark",
                    },
                    "Contact",
                    key="email",
                )
            ]
            if app.author_email
            else [],
            [
                button(
                    {
                        "className": "btn btn-sm btn-primary",
                        "onClick": lambda x: print("clicked"),
                    },
                    "Install",
                    key="install",
                )
            ]
            if installable.data
            else [],
        ),
        div({"className": "description"}, app.short_description),
        div(
            {"className": "background"}
            | (
                {"style": {"backgroundImage": f'url("{app.background.url}")'}}
                if app.background
                else {}
            )
        ),
    )
