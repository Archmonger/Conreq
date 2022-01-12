from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from conreq import config
from conreq._core.initialization.views import initialize
from conreq.app import register
from conreq.utils.environment import get_base_url, get_debug, get_home_url

BASE_URL = get_base_url()
HOME_URL = get_home_url()
DEBUG = get_debug()


@register.view.home()
def home(request):
    """Renders the homepage."""
    # Render the home page
    return initialize(request) or login_required(render)(
        request,
        config.templates.home,
        {
            "base_url": BASE_URL,
            "home_url": HOME_URL,
            "debug": DEBUG,
        },
    )
