import asyncio
import random

from reactpy import component, hooks
from reactpy.html import a, button, div, h5

from conreq._core.app_store.components.event import (
    author_click_event,
    details_modal_event,
    subcategory_click_event,
)
from conreq._core.app_store.components.modal import package_install_modal
from conreq._core.app_store.models import AppPackage, Subcategory
from conreq.types import AppStoreStateContext, ModalState, ModalStateContext


@component
def card(app: AppPackage):
    modal_state = hooks.use_context(ModalStateContext)
    animation_speed, _ = hooks.use_state(random.randint(7, 13))
    opacity, set_opacity = hooks.use_state(0)

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
        card_top(app, app.subcategories.all()[0]),
        card_btns(app, modal_state),
        div({"class_name": "description"}, app.short_description),
        card_background(app),
    )


def card_top(app: AppPackage, subcategory: Subcategory | None):
    state = hooks.use_context(AppStoreStateContext)

    return div(
        {"class_name": "top"},
        div(
            {"class_name": "text-region"},
            h5(
                {"class_name": "card-title"},
                app.name,
            ),
            [
                div(
                    {"class_name": "card-author", "key": "author"},
                    a(
                        {"href": "#", "on_click": author_click_event(state, app)},
                        app.author,
                    ),
                )
            ]
            if app.author
            else [],
            [
                div(
                    {"class_name": "card-category", "key": "category"},
                    a(
                        {
                            "href": "#",
                            "on_click": subcategory_click_event(state, subcategory),
                        },
                        str(subcategory) if subcategory else "",
                    ),
                )
            ]
            if subcategory
            else [],
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


def card_btns(app: AppPackage, modal_state: ModalState):
    async def install_click(_):
        modal_state.show = True
        modal_state.modal_intent = package_install_modal
        modal_state.args = [app]
        modal_state.set_state(modal_state)

    return div(
        {"class_name": "btn-container"},
        button(
            {
                "class_name": "btn btn-sm btn-dark",
                "on_click": details_modal_event(modal_state, app),
            },
            "Details",
        ),
        a(
            {
                "href": f"{app.contact_link}" or f"mailto:{app.contact_email}",
                "class_name": "btn btn-sm btn-dark",
                "key": "email",
            },
            "Contact",
        )
        if app.contact_link or app.contact_email
        else "",
        button(
            {
                "class_name": "btn btn-sm btn-primary",
                "on_click": install_click,
                "key": "install",
            },
            "Install",
        )
        if app.compatible and not app.installed
        else button(
            {
                "class_name": "btn btn-sm btn-primary",
                "disabled": True,
                "key": "installed",
            },
            "Installed",
        )
        if app.installed
        else "",
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
