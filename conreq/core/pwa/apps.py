""" Settings required by django-app. """
import os

from django.apps import AppConfig
from django.conf import settings
from django.shortcuts import resolve_url
from django.urls import get_script_prefix
from django.utils.functional import lazy

from conreq.utils.environment import get_base_url

# Lazy-evaluate URLs so including pwa.urls in root urlconf works
resolve_url = lazy(resolve_url, str)

# Get script prefix for apps not mounted under /
_PWA_SCRIPT_PREFIX = get_script_prefix()


class PwaConfig(AppConfig):
    name = "conreq.core.pwa"

    # Path to the service worker implementation.  Default implementation is empty.
    SERVICE_WORKER_PATH = getattr(
        settings,
        "PWA_SERVICE_WORKER_PATH",
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "templates", "serviceworker.js"
        ),
    )
    # App parameters to include in site.webmanifest and appropriate meta tags
    APP_NAME = getattr(settings, "PWA_APP_NAME", "MyApp")
    APP_DESCRIPTION = getattr(settings, "PWA_APP_DESCRIPTION", "My Progressive Web App")
    APP_ROOT_URL = resolve_url(
        getattr(settings, "PWA_APP_ROOT_URL", _PWA_SCRIPT_PREFIX)
    )
    APP_THEME_COLOR = getattr(settings, "PWA_APP_THEME_COLOR", "#000")
    APP_BACKGROUND_COLOR = getattr(settings, "PWA_APP_BACKGROUND_COLOR", "#fff")
    APP_DISPLAY = getattr(settings, "PWA_APP_DISPLAY", "standalone")
    APP_SCOPE = resolve_url(getattr(settings, "PWA_APP_SCOPE", _PWA_SCRIPT_PREFIX))
    APP_DEBUG_MODE = getattr(settings, "PWA_APP_DEBUG_MODE", True)
    APP_ORIENTATION = getattr(settings, "PWA_APP_ORIENTATION", "any")
    APP_START_URL = resolve_url(
        getattr(settings, "PWA_APP_START_URL", _PWA_SCRIPT_PREFIX)
    )
    APP_FETCH_URL = resolve_url(
        getattr(settings, "PWA_APP_FETCH_URL", _PWA_SCRIPT_PREFIX)
    )
    APP_STATUS_BAR_COLOR = getattr(settings, "PWA_APP_STATUS_BAR_COLOR", "default")
    APP_ICONS = getattr(settings, "PWA_APP_ICONS", [])
    APP_ICONS_APPLE = getattr(settings, "PWA_APP_ICONS_APPLE", [])
    APP_SPLASH_SCREEN = getattr(settings, "PWA_APP_SPLASH_SCREEN", [])
    APP_DIR = getattr(settings, "PWA_APP_DIR", "auto")
    APP_LANG = getattr(settings, "PWA_APP_LANG", "en-US")
    BASE_URL = get_base_url()
