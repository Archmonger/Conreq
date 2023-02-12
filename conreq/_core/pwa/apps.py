""" Settings required by django-app. """


from django.apps import AppConfig
from django.conf import settings

from conreq.utils.environment import get_base_url


class PwaConfig(AppConfig):
    name = "conreq._core.pwa"

    # Parameters to include in site.webmanifest and appropriate meta tags

    app_name = "Conreq"
    app_description = "A hub for great things."
    app_theme_color = "#3fcfa6"
    app_background_color = "#04110d"
    app_display = "standalone"
    app_start_url = get_base_url()
    app_scope = get_base_url()
    app_debug_mode = settings.DEBUG
    app_orientation = "any"
    app_status_bar_color = "default"
    app_icons = [
        {
            "src": f"{get_base_url()}static/conreq/icons/standard.png",
            "sizes": "512x512",
            "purpose": "any",
        },
        {
            "src": f"{get_base_url()}static/conreq/icons/maskable.png",
            "sizes": "512x512",
            "purpose": "maskable",
        },
    ]

    app_icons_apple = [
        {
            "src": f"{get_base_url()}static/conreq/icons/apple-touch-icon.png",
            "sizes": "180x180",
        }
    ]

    app_splash_screen: list[str] = []
    app_dir = "auto"
    app_lang = "en-US"
