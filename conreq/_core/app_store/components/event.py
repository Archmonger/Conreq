from conreq._core.app_store.components.query import (
    get_author_apps,
    get_category_apps,
    get_subcategory_apps,
)
from conreq._core.app_store.models import AppPackage, Category, Subcategory
from conreq.types import AppStoreState, ModalState


def author_click_event(state: AppStoreState, app: AppPackage):
    async def event(_):
        # pylint: disable=import-outside-toplevel
        from conreq._core.app_store.components.filtered import filtered_cards

        state.tab = filtered_cards
        state.tab_args = (await get_author_apps(app.author),)
        state.set_state(state)

    return event


def details_modal_event(state: ModalState, app: AppPackage):
    async def event(_):
        # pylint: disable=import-outside-toplevel
        from conreq._core.app_store.components.modal import package_details_modal

        state.show = True
        state.modal_intent = package_details_modal
        state.modal_args = [app]
        state.set_state(state)

    return event


def subcategory_click_event(state: AppStoreState, subcategory: Subcategory):
    async def event(_):
        # pylint: disable=import-outside-toplevel
        from conreq._core.app_store.components.filtered import filtered_cards

        state.tab = filtered_cards
        state.tab_args = (await get_subcategory_apps(subcategory),)
        state.set_state(state)

    return event


def category_click_event(state: AppStoreState, category: Category):
    async def event(_):
        # pylint: disable=import-outside-toplevel
        from conreq._core.app_store.components.filtered import filtered_cards

        state.tab = filtered_cards
        state.tab_args = (await get_category_apps(category),)
        state.set_state(state)

    return event
