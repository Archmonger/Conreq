from conreq.apps.base.forms import InitializationForm
from conreq.apps.server_settings.models import ConreqConfig
from conreq.utils.apps import generate_context, initialize_conreq
from conreq.utils.generic import get_base_url
from conreq.utils.testing import render_async, performance_metrics
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

BASE_URL = get_base_url()

# Create your views here.
@render_async
@performance_metrics()
def initialization(request):
    conreq_config = ConreqConfig.get_solo()
    user_objects = get_user_model().objects

    # Authenticate using Organizr headers
    organizr_username = request.headers.get("X-WEBAUTH-USER")
    if conreq_config.conreq_http_header_auth and organizr_username:
        organizr_email = request.headers.get("X-WEBAUTH-EMAIL")
        organizr_group = int(request.headers.get("X-WEBAUTH-GROUP"))
        user = user_objects.get_or_create(
            username=organizr_username,
        )[0]
        user.email = organizr_email
        user.is_staff = False
        if organizr_group == 0:
            user.is_superuser = True
        if organizr_group == 0 or organizr_group == 1:
            user.is_staff = True
        user.save()
        login(request, user)

    # Run the first time initialization if needed
    if conreq_config.conreq_initialized is False:

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
                initialize_conreq(conreq_config, form)
                return redirect("base:index")

            # Form data wasn't valid, so return the error codes
            template = loader.get_template("registration/initialization.html")
            return HttpResponse(template.render({"form": form}, request))

        # User needs to fill out the first time setup
        template = loader.get_template("registration/initialization.html")
        return HttpResponse(template.render({}, request))

    # If a base URL is set, redirect the user to it
    if request.path[1:] != BASE_URL:
        return redirect("/" + BASE_URL)

    # Render the base
    return login_required(render)(request, "primary/base.html", generate_context({}))
