from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from conreq import config
from conreq._core.initialization.views import initialize


def home(request):
    """Renders the homepage."""
    # Render the home page
    return initialize(request) or login_required(render)(
        request, config.templates.home, {"home_config": config.homepage}
    )
