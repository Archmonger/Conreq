from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from conreq.core.server_settings.models import ConreqConfig

from .forms import InitializationForm


def initialize(request):
    conreq_config = ConreqConfig.get_solo()

    # Run the first time initialization if needed
    if conreq_config.initialized is False:

        # User submitted the first time setup form
        if request.method == "POST":

            form = InitializationForm(request.POST)

            # Create the superuser and set up the database if the form is valid
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=password)
                user.is_staff = True
                user.is_admin = True
                user.is_superuser = True
                user.save()
                login(request, user)
                conreq_config.initialized = True
                conreq_config.save()
                return redirect("base:landing")

            # Form data wasn't valid, so return the error codes
            template = loader.get_template("registration/initialization.html")
            return HttpResponse(template.render({"form": form}, request))

        # User needs to fill out the first time setup
        template = loader.get_template("registration/initialization.html")
        return HttpResponse(template.render({}, request))

    return None
