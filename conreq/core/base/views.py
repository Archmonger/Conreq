from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from conreq.core.first_run.views import initialize
from conreq.utils.debug import performance_metrics
from conreq.utils.environment import get_base_url, get_debug

BASE_URL = get_base_url()
DEBUG = get_debug()
LANDING_TEMPLATE = None
HOME_TEMPLATE = "primary/base_app.html"


@performance_metrics()
def landing(request):
    """The primary view that handles whether to take the user to
    login, splash, initialization, or homepage."""

    initialization_needed = initialize(request)

    if initialization_needed:
        return initialization_needed

    if not LANDING_TEMPLATE:
        return redirect("base:homescreen")

    # Render the landing page
    return render(request, LANDING_TEMPLATE, {"base_url": BASE_URL, "debug": DEBUG})


@performance_metrics()
def home(request):
    """The primary view that handles whether to take the user to
    login, splash, initialization, or homepage."""

    initialization_needed = initialize(request)

    if initialization_needed:
        return initialization_needed

    # Render the home page
    return login_required(render)(
        request, HOME_TEMPLATE, {"base_url": BASE_URL, "debug": DEBUG}
    )
