from django.contrib import auth
from django.shortcuts import render

from conreq import AuthLevel
from conreq.utils.components import view_to_component


@view_to_component(name="logout_parent_frame", auth_level=AuthLevel.anonymous)
def logout(request=None):
    """Logs a user out, then triggers a `reload-page` event on the current page."""
    auth.logout(request)
    return render(request, "conreq/refresh_parent_frame.html", {})


@view_to_component(name="refresh_parent_frame", auth_level=AuthLevel.anonymous)
def refresh(request=None):
    """Triggers a `reload-page` event on the current page."""
    logout(request)
    return render(request, "conreq/refresh_parent_frame.html", {})
