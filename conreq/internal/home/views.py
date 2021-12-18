from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import conreq
from conreq.app import register
from conreq.internal.first_run.views import initialize
from conreq.utils.environment import get_base_url, get_debug, get_home_url

BASE_URL = get_base_url()
HOME_URL = get_home_url()
DEBUG = get_debug()


@register.home_view()
def home(request):
    """Renders the homepage."""
    # Render the home page
    return initialize(request) or login_required(render)(
        request,
        conreq.config.home_template,
        {
            "base_url": BASE_URL,
            "home_url": HOME_URL,
            "debug": DEBUG,
            "app_config": conreq.config,
        },
    )
