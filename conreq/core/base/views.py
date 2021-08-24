from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from conreq.core.base.forms import InitializationForm
from conreq.core.server_settings.models import ConreqConfig
from conreq.utils.debug import performance_metrics
from conreq.utils.environment import get_base_url, get_debug

from .helpers import initialize_conreq

BASE_URL = get_base_url()
DEBUG = get_debug()
LANDING_TEMPLATE = None
HOME_TEMPLATE = "primary/base_app.html"


def configure(request):
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
                initialize_conreq(conreq_config, form)
                return redirect("base:landing")

            # Form data wasn't valid, so return the error codes
            template = loader.get_template("registration/initialization.html")
            return HttpResponse(template.render({"form": form}, request))

        # User needs to fill out the first time setup
        template = loader.get_template("registration/initialization.html")
        return HttpResponse(template.render({}, request))


@cache_page(30)
@vary_on_cookie
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
    return render(request, LANDING_TEMPLATE, {"base_url": BASE_URL, "debug": DEBUG})


@cache_page(30)
@vary_on_cookie
@performance_metrics()
def home(request):
    """The primary view that handles whether to take the user to
    login, splash, initialization, or homepage."""

    config_needed = configure(request)

    if config_needed:
        return config_needed

    # Render the home page
    return login_required(render)(
        request, HOME_TEMPLATE, {"base_url": BASE_URL, "debug": DEBUG}
    )
