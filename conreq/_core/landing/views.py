from django.shortcuts import redirect, render

from conreq import config
from conreq._core.initialization.views import initialize


def landing(request):
    """Renders the landing page (if available)."""
    # sourcery skip: assign-if-exp
    # Redirect if a landing page doesn't exist
    if not config.templates.landing:
        return redirect("conreq:home")

    # Render the landing page
    return initialize(request) or render(request, config.templates.landing)
