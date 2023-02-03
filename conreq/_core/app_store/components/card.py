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
        card_top(app, modal_state, app.subcategories.all()[0]),
        card_btns(app, modal_state, installable.data),
        div(app.short_description, class_name="description"),
        card_background(app),
        class_name="card fade-in" + (" special" if app.special else ""),
        style={"opacity": opacity}
        | ({"--animation-speed": f"{animation_speed}s"} if app.special else {}),
    )


def card_top(app: AppPackage, modal_state: ModalState, subcategory: Subcategory | None):
    return div(
        div(
            h5(
                a(
                    app.name,
                    href=f"#{app.uuid}",
                    on_click=details_modal_event(modal_state, app),
                ),
                class_name="card-title",
            ),
            [
                div(
                    a(app.author, href="#", on_click=lambda x: print("clicked")),
                    key="author",
                    class_name="card-author",
                )
            ]
            if app.author
            else [],
            div(
                a(
                    str(subcategory) if subcategory else "",
                    href="#",
                    on_click=lambda x: print("clicked"),
                ),
                class_name="card-category",
            ),
            class_name="text-region",
        ),
        div(
            **(
                {"class_name": "logo"}
                | (
                    {"style": {"background_image": f'url("{app.logo.url}")'}}
                    if app.logo
                    else {}
                )
            ),
        ),
        class_name="top",
    )


def card_btns(app: AppPackage, modal_state: ModalState, installable: bool | None):
    return div(
        button(
            "Details",
            class_name="btn btn-sm btn-dark",
            on_click=details_modal_event(modal_state, app),
        ),
        [
            a(
                "Contact",
                key="email",
                href=f"{app.contact_link}" or f"mailto:{app.contact_email}",
                class_name="btn btn-sm btn-dark",
            )
        ]
        if app.contact_link or app.contact_email
        else [],
        [
            button(
                "Install",
                key="install",
                class_name="btn btn-sm btn-primary",
                on_click=lambda x: print("clicked"),
            )
        ]
        if installable
        else [],
        class_name="btn-container",
    )


def card_background(app: AppPackage):
    return div(
        **(
            {"class_name": "background"}
            | (
                {"style": {"backgroundImage": f'url("{app.background.url}")'}}
                if app.background
                else {}
            )
        ),
    )
