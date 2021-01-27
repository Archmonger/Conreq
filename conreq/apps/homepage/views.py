from conreq.apps.server_settings.models import ConreqConfig
from conreq.utils.apps import (
    generate_context,
    initialize_admin_account,
    initialize_database,
)
from conreq.utils.generic import get_base_url
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
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

            # Set up the initial database values
            initialize_database(conreq_config, request)

            # Save values to the database if they're valid
            try:
                conreq_config.clean_fields()
                initialize_admin_account(request)
                # conreq_config.save()

            except ValidationError as issues:
                print(vars(issues))
                # template = loader.get_template("initialization/first_run.html")
                # return HttpResponse(
                #     template.render({"form_errors": issues.error_dict}, request)
                # )

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
