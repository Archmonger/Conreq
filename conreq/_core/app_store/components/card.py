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
            "class_name": "card fade-in" + (" special" if app.special else ""),
            "style": {"opacity": opacity}
            | ({"--animation-speed": f"{animation_speed}s"} if app.special else {}),
        },
        card_top(app, modal_state, app.subcategories.all()[0]),
        card_btns(app, modal_state, installable.data),
        div({"class_name": "description"}, app.short_description),
        card_background(app),
    )


def card_top(app: AppPackage, modal_state: ModalState, subcategory: Subcategory | None):
    return div(
        {"class_name": "top"},
        div(
            {"class_name": "text-region"},
            h5(
                {"class_name": "card-title"},
                a(
                    {
                        "href": f"#{app.uuid}",
                        "on_click": details_modal_event(modal_state, app),
                    },
                    app.name,
                ),
            ),
            [
                div(
                    {"class_name": "card-author", "key": "author"},
                    a(
                        {"href": "#", "on_click": lambda x: print("clicked")},
                        app.author,
                    ),
                )
            ]
            if app.author
            else [],
            div(
                {"class_name": "card-category"},
                a(
                    {"href": "#", "on_click": lambda x: print("clicked")},
                    str(subcategory) if subcategory else "",
                ),
            ),
        ),
        div(
            {"class_name": "logo"}
            | (
                {"style": {"background_image": f'url("{app.logo.url}")'}}
                if app.logo
                else {}
            )
        ),
    )


def card_btns(app: AppPackage, modal_state: ModalState, installable: bool | None):
    return div(
        {"class_name": "btn-container"},
        button(
            {
                "class_name": "btn btn-sm btn-dark",
                "on_click": details_modal_event(modal_state, app),
            },
            "Details",
        ),
        [
            a(
                {
                    "href": f"{app.contact_link}" or f"mailto:{app.contact_email}",
                    "class_name": "btn btn-sm btn-dark",
                    "key": "email",
                },
                "Contact",
            )
        ]
        if app.contact_link or app.contact_email
        else [],
        [
            button(
                {
                    "class_name": "btn btn-sm btn-primary",
                    "on_click": lambda x: print("clicked"),
                    "key": "install",
                },
                "Install",
            )
        ]
        if installable
        else [],
    )


def card_background(app: AppPackage):
    return div(
        {"class_name": "background"}
        | (
            {"style": {"background_image": f'url("{app.background.url}")'}}
            if app.background
            else {}
        )
    )
