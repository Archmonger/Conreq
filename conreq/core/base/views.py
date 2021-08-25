from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from conreq.core.first_run.views import initialize
from conreq.utils.debug import performance_metrics
from conreq.utils.environment import get_base_url, get_debug
from conreq import app

BASE_URL = get_base_url()
DEBUG = get_debug()


@performance_metrics()
def landing(request):
    """Renders the landing page (if available)."""

    initialization_needed = initialize(request)
    landing_template = app.config("landing_template")

    if initialization_needed:
        return initialization_needed

    if not landing_template:
        return redirect("base:home")

    # Render the landing page
    return render(request, landing_template, {"base_url": BASE_URL, "debug": DEBUG})


@performance_metrics()
def home(request):
    """Renders the homepage."""

    initialization_needed = initialize(request)

    if initialization_needed:
        return initialization_needed

    # Render the home page
    return login_required(render)(
        request, app.config("home_template"), {"base_url": BASE_URL, "debug": DEBUG}
    )
