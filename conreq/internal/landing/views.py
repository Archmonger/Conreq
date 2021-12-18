from django.shortcuts import redirect, render

import conreq
from conreq.app import register
from conreq.internal.first_run.views import initialize
from conreq.utils.environment import get_base_url, get_debug, get_home_url

BASE_URL = get_base_url()
HOME_URL = get_home_url()
DEBUG = get_debug()


@register.landing_view()
def landing(request):
    """Renders the landing page (if available)."""
    # Redirect if a landing page doesn't exist
    if not conreq.config.landing_template:
        return redirect("home")

    # Render the landing page
    return initialize(request) or render(
        request,
        conreq.config.landing_template,
        {
            "base_url": BASE_URL,
            "home_url": HOME_URL,
            "debug": DEBUG,
            "app_config": conreq.config,
        },
    )
