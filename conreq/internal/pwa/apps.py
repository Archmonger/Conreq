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
    app_name = "Conreq"
    app_description = "A hub for great things."
    app_theme_color = "#3fcfa6"
    app_background_color = "#04110d"
    app_display = "standalone"
    app_start_url = resolve_url(settings.BASE_URL)
    app_scope = resolve_url(settings.BASE_URL)
    app_debug_mode = settings.DEBUG
    app_orientation = "any"
    app_status_bar_color = "default"
    app_icons = [
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
    app_icons_apple = [
        {
            "src": settings.BASE_URL + "static/icons/apple-touch-icon.png",
            "sizes": "180x180",
        }
    ]
    app_splash_screen = []
    app_dir = "auto"
    app_lang = "en-US"
