from conreq.apps.homepage.forms import initializationForm
from conreq.apps.server_settings.models import ConreqConfig
from conreq.utils.apps import generate_context, initialize_conreq
from conreq.utils.generic import get_base_url
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.cache import cache_page

BASE_URL = get_base_url()

# Create your views here.
def initialization(request):
    conreq_config = ConreqConfig.get_solo()

    # Run the first time initialization if needed
    if conreq_config.conreq_initialized is False:

        # User submitted the first time setup form
        if request.method == "POST":

            form = initializationForm(request.POST)

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
                return redirect("homepage:index")

            # Form data wasn't valid, so return the error codes
            template = loader.get_template("initialization/first_run.html")
            return HttpResponse(template.render({"form": form}, request))

        # User needs to fill out the first time setup
        template = loader.get_template("initialization/first_run.html")
        return HttpResponse(template.render({}, request))

    # If a base URL is set, redirect the user to it
    if request.path[1:] != BASE_URL:
        return redirect("/" + BASE_URL)

    # Render the homepage
    return homepage(request)


@cache_page(1)
@login_required
def homepage(request):
    # Generate the base template
    template = loader.get_template("primary/base.html")
    context = generate_context({})
    return HttpResponse(template.render(context, request))
