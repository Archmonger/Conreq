from typing import Iterable

from reactpy import component
from reactpy.html import div
from reactpy_django.components import django_css

from conreq._core.app_store.components.card import card
from conreq._core.app_store.models import AppPackage


@component
def filtered_cards(apps: Iterable[AppPackage]):
    """Displays a list of apps as cards."""

    return div(
        {"class_name": "filtered-cards"},
        django_css("conreq/app_store_filtered.css"),
        django_css("conreq/app_store_card.css"),
        [card(app, key=app.uuid) for app in apps] if apps else "Nothing found!",
    )
