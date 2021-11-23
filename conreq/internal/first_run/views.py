from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from conreq.internal.server_settings.models import ServerConfig
from conreq.utils.environment import get_env, set_env

from .forms import InitializationForm


def initialize(request):
    server_config = ServerConfig.get_solo()

    # Run the first time initialization if needed
    if server_config.initialized is True:
        return False

    # User submitted the first time setup form
    if request.method == "POST":

        form = InitializationForm(request.POST)

        # Create the superuser and set up the database if the form is valid
        if form.is_valid():
            return _first_run_setup(form, request, server_config)

        # Form data wasn't valid, so return the error codes
        template = loader.get_template("registration/initialization.html")
        return HttpResponse(template.render({"form": form}, request))

    # User needs to fill out the first time setup
    template = loader.get_template("registration/initialization.html")
    return HttpResponse(template.render({}, request))


def _first_run_setup(form, request, server_config):
    form.save()
    username = form.cleaned_data.get("username")
    password = form.cleaned_data.get("password1")
    user = authenticate(username=username, password=password)
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.save()
    login(request, user)
    server_config.initialized = True
    server_config.save()
    if get_env("COMPRESS_RESPONSES", return_type=bool) is None:
        set_env("COMPRESS_RESPONSES", "true")
    return redirect("landing")
