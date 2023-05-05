from typing import Iterable

from reactpy import component
from reactpy.html import div

from conreq._core.app_store.components.card import card
from conreq._core.app_store.models import AppPackage


@component
def filtered_card_view(apps: Iterable[AppPackage]):
    """Displays a list of apps as cards."""

    return div(
        {"class_name": "card-view"},
        [card(app, key=app.uuid) for app in apps] if apps else "Nothing found!",
    )
