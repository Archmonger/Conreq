from typing import Union

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from conreq.internal.first_run.models import Initialization

from .forms import InitializationForm

INITIALIZED = False


def initialize(request) -> Union[None, HttpResponse]:
    # pylint: disable=global-statement
    # Check cached value if we've already initialized
    global INITIALIZED
    if INITIALIZED:
        return None

    # Run the first time initialization if needed
    initialization = Initialization.get_solo()
    if initialization.initialized:
        INITIALIZED = True
        return None

    # User submitted the first time setup form
    if request.method == "POST":
        form = InitializationForm(request.POST)

        # Create the superuser and set up the database if the form is valid
        if form.is_valid():
            return _first_run_setup(form, request, initialization)

        # Form data wasn't valid, so return the error codes
        template = loader.get_template("conreq/registration/initialization.html")
        return HttpResponse(template.render({"form": form}, request))

    # User needs to fill out the first time setup
    template = loader.get_template("conreq/registration/initialization.html")
    return HttpResponse(template.render({}, request))


def _first_run_setup(form, request, general_settings):
    form.save()
    username = form.cleaned_data.get("username")
    password = form.cleaned_data.get("password1")
    user = authenticate(username=username, password=password)
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.save()
    login(request, user)
    general_settings.initialized = True
    general_settings.save()
    return redirect("landing")
