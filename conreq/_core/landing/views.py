from django.shortcuts import redirect, render

from conreq import config
from conreq._core.initialization.views import initialize
from conreq.app import register
from conreq.utils.environment import get_base_url, get_debug, get_home_url

BASE_URL = get_base_url()
HOME_URL = get_home_url()
DEBUG = get_debug()


@register.view.landing()
def landing(request):
    """Renders the landing page (if available)."""
    # Redirect if a landing page doesn't exist
    if not config.templates.landing:
        return redirect("home")

    # Render the landing page
    return initialize(request) or render(
        request,
        config.templates.landing,
        {
            "base_url": BASE_URL,
            "home_url": HOME_URL,
            "debug": DEBUG,
        },
    )
