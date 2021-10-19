""" Settings required by django-app. """
import os

from django.apps import AppConfig
from django.conf import settings
from django.shortcuts import resolve_url as _resolve
from django.utils.functional import lazy

# Lazy-evaluate URLs so including pwa.urls in root urlconf works
resolve_url = lazy(_resolve, str)


class PwaConfig(AppConfig):
    name = "conreq.internal.pwa"

    # Path to the service worker implementation.  Default implementation is empty.
    SERVICE_WORKER_PATH = getattr(
        settings,
        "PWA_SERVICE_WORKER_PATH",
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "templates", "serviceworker.js"
        ),
    )

    # Parameters to include in site.webmanifest and appropriate meta tags
    APP_NAME = "Conreq"
    APP_DESCRIPTION = "A hub for great things."
    APP_THEME_COLOR = "#3fcfa6"
    APP_BACKGROUND_COLOR = "#04110d"
    APP_DISPLAY = "standalone"
    APP_START_URL = resolve_url(settings.BASE_URL)
    APP_SCOPE = resolve_url(settings.BASE_URL)
    APP_DEBUG_MODE = settings.DEBUG
    APP_ORIENTATION = "any"
    APP_STATUS_BAR_COLOR = "default"
    APP_ICONS = [
        {
            "src": settings.BASE_URL + "static/icons/standard.png",
            "sizes": "512x512",
            "purpose": "any",
        },
        {
            "src": settings.BASE_URL + "static/icons/maskable.png",
            "sizes": "512x512",
            "purpose": "maskable",
        },
    ]
    APP_ICONS_APPLE = [
        {
            "src": settings.BASE_URL + "static/icons/apple-touch-icon.png",
            "sizes": "180x180",
        }
    ]
    APP_SPLASH_SCREEN = []
    APP_DIR = "auto"
    APP_LANG = "en-US"
