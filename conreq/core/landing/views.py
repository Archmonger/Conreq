from django.shortcuts import redirect, render

from conreq import app
from conreq.core.first_run.views import initialize
from conreq.utils.environment import get_base_url, get_debug, get_home_url

BASE_URL = get_base_url()
HOME_URL = get_home_url()
DEBUG = get_debug()


@app.register.landing_view()
def landing(request):
    """Renders the landing page (if available)."""

    initialization_needed = initialize(request)
    landing_template = app.config.landing_template

    if initialization_needed:
        return initialization_needed

    if not landing_template:
        return redirect("home:main")

    # Render the landing page
    return render(
        request,
        landing_template,
        {
            "base_url": BASE_URL,
            "home_url": HOME_URL,
            "debug": DEBUG,
            "app_config": app.config,
        },
    )