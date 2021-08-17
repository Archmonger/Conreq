from conreq.core.base.forms import InitializationForm
from conreq.core.server_settings.models import ConreqConfig
from conreq.utils.environment import get_base_url, get_debug_from_env
from conreq.utils.debug import performance_metrics
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .helpers import initialize_conreq

BASE_URL = get_base_url()
DEBUG = get_debug_from_env()
LANDING_TEMPLATE = None
HOME_TEMPLATE = "primary/base_app.html"


def configure(request):
    user_objects = get_user_model().objects
    conreq_config = ConreqConfig.get_solo()

    # Authenticate using Organizr headers
    # TODO: Turn this into a middleware app
    organizr_username = request.headers.get("X-WEBAUTH-USER")
    if conreq_config.conreq_http_header_auth and organizr_username:
        # Configure the user parameters
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
        if user.has_usable_password():
            user.set_unusable_password()
        user.save()

        # Make sure the user is labeled as a HTTP auth user
        if not user.profile.externally_authenticated:
            user.profile.externally_authenticated = True
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
                return redirect("base:landing")

            # Form data wasn't valid, so return the error codes
            template = loader.get_template("registration/initialization.html")
            return HttpResponse(template.render({"form": form}, request))

        # User needs to fill out the first time setup
        template = loader.get_template("registration/initialization.html")
        return HttpResponse(template.render({}, request))


@performance_metrics()
def landing(request):
    """The primary view that handles whether to take the user to
    login, splash, initialization, or homepage."""

    config_needed = configure(request)

    if config_needed:
        return config_needed

    if not LANDING_TEMPLATE:
        return redirect("base:homescreen")

    # Render the landing page
    return login_required(render)(
        request, LANDING_TEMPLATE, {"base_url": BASE_URL, "debug": DEBUG}
    )


@performance_metrics()
def home(request):
    """The primary view that handles whether to take the user to
    login, splash, initialization, or homepage."""
    conreq_config = ConreqConfig.get_solo()
    user_objects = get_user_model().objects

    # Authenticate using Organizr headers
    organizr_username = request.headers.get("X-WEBAUTH-USER")
    if conreq_config.conreq_http_header_auth and organizr_username:
        # Configure the user parameters
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
        if user.has_usable_password():
            user.set_unusable_password()
        user.save()

        # Make sure the user is labeled as a HTTP auth user
        if not user.profile.externally_authenticated:
            user.profile.externally_authenticated = True
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
                return redirect("base:landing")

            # Form data wasn't valid, so return the error codes
            template = loader.get_template("registration/initialization.html")
            return HttpResponse(template.render({"form": form}, request))

        # User needs to fill out the first time setup
        template = loader.get_template("registration/initialization.html")
        return HttpResponse(template.render({}, request))

    # Render the base
    return login_required(render)(
        request, HOME_TEMPLATE, {"base_url": BASE_URL, "debug": DEBUG}
    )
