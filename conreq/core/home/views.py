from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from conreq import app
from conreq.core.first_run.views import initialize
from conreq.utils.environment import get_base_url, get_debug, get_home_url

BASE_URL = get_base_url()
HOME_URL = get_home_url()
DEBUG = get_debug()


@app.register.home_view()
def home(request):
    """Renders the homepage."""

    initialization_needed = initialize(request)
    home_template = app.config.home_template

    if initialization_needed:
        return initialization_needed

    # Render the home page
    return login_required(render)(
        request,
        home_template,
        {
            "base_url": BASE_URL,
            "home_url": HOME_URL,
            "debug": DEBUG,
            "app_config": app.config,
        },
    )
