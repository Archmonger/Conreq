from django.contrib.auth import logout
from django.shortcuts import render
from conreq.app.selectors import AuthLevel

from conreq.utils.components import view_to_component


@view_to_component(name="logout_parent_frame", auth_level=AuthLevel.anonymous)
def logout_parent_frame(request=None):
    logout(request)
    return render(request, "conreq/refresh_parent_frame.html", {})


@view_to_component(name="refresh_parent_frame", auth_level=AuthLevel.anonymous)
def refresh_parent_frame(request=None):
    logout(request)
    return render(request, "conreq/refresh_parent_frame.html", {})
