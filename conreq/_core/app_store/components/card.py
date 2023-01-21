import asyncio
import random

from django_idom.hooks import use_query
from django_idom.types import QueryOptions
from idom import component, hooks
from idom.html import a, button, div, h5

from conreq._core.app_store.components.modal import app_modal
from conreq._core.app_store.models import AppPackage, Subcategory
from conreq.types import ModalState, ModalStateContext


def details_modal_event(modal_state: ModalState, app: AppPackage):
    async def event(_):
        modal_state.show = True
        modal_state.modal_intent = app_modal
        modal_state.modal_args = [app]
        modal_state.set_state(modal_state)

    return event


def check_installable(app: AppPackage):
    return app.installable


@component
def card(app: AppPackage):
    modal_state = hooks.use_context(ModalStateContext)
    animation_speed, _ = hooks.use_state(random.randint(7, 13))
    opacity, set_opacity = hooks.use_state(0)
    installable = use_query(QueryOptions(postprocessor=None), check_installable, app)

    @hooks.use_effect(dependencies=[])
    async def fade_in_animation():
        await asyncio.sleep(round(random.uniform(0, 0.55), 3))
        set_opacity(1)

    return div(
        {
            "className": "card fade-in" + (" special" if app.special else ""),
            "style": {"opacity": opacity}
            | ({"--animation-speed": f"{animation_speed}s"} if app.special else {}),
        },
        card_top(app, modal_state, app.subcategories.all()[0]),
        card_btns(app, modal_state, installable.data),
        div({"className": "description"}, app.short_description),
        card_background(app),
    )


def card_top(app: AppPackage, modal_state: ModalState, subcategory: Subcategory | None):
    return div(
        {"className": "top"},
        div(
            {"className": "text-region"},
            h5(
                {"className": "card-title"},
                a(
                    {
                        "href": f"#{app.uuid}",
                        "onClick": details_modal_event(modal_state, app),
                    },
                    app.name,
                ),
            ),
            [
                div(
                    {"className": "card-author"},
                    a(
                        {"href": "#", "onClick": lambda x: print("clicked")},
                        app.author,
                    ),
                    key="author",
                )
            ]
            if app.author
            else [],
            div(
                {"className": "card-category"},
                a(
                    {"href": "#", "onClick": lambda x: print("clicked")},
                    str(subcategory) if subcategory else "",
                ),
            ),
        ),
        div(
            {"className": "logo"}
            | (
                {"style": {"backgroundImage": f'url("{app.logo.url}")'}}
                if app.logo
                else {}
            )
        ),
    )


def card_btns(app: AppPackage, modal_state: ModalState, installable: bool | None):
    return div(
        {"className": "btn-container"},
        button(
            {
                "className": "btn btn-sm btn-dark",
                "onClick": details_modal_event(modal_state, app),
            },
            "Details",
        ),
        [
            a(
                {
                    "href": f"{app.contact_link}" or f"mailto:{app.contact_email}",
                    "className": "btn btn-sm btn-dark",
                },
                "Contact",
                key="email",
            )
        ]
        if app.contact_link or app.contact_email
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
        if installable
        else [],
    )


def card_background(app: AppPackage):
    return div(
        {"className": "background"}
        | (
            {"style": {"backgroundImage": f'url("{app.background.url}")'}}
            if app.background
            else {}
        )
    )
