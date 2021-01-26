import secrets

from conreq.apps.server_settings.models import ConreqConfig
from conreq.utils.apps import generate_context
from conreq.utils.generic import get_base_url
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.cache import cache_page

BASE_URL = get_base_url()

# Create your views here.
def initialization(request):
    conreq_config = ConreqConfig.get_solo()
    config_has_changed = False

    # Ensure API key is configured
    if not conreq_config.conreq_api_key:
        conreq_config.conreq_api_key = secrets.token_hex(16)
        config_has_changed = True

    # Ensure URL or API key is configured if sonarr is enabled
    if (
        not conreq_config.sonarr_url or not conreq_config.sonarr_api_key
    ) and conreq_config.sonarr_enabled:
        conreq_config.sonarr_enabled = False
        config_has_changed = True

    # Ensure URL or API key is configured if radarr is enabled
    if (
        not conreq_config.radarr_url or not conreq_config.radarr_api_key
    ) and conreq_config.radarr_enabled:
        conreq_config.radarr_enabled = False
        config_has_changed = True

    # Save the new values if things have changed
    if config_has_changed:
        conreq_config.save()

    # Run the first time initialization if needed
    if conreq_config.conreq_initialized is False:
        pass
        # Display the first run template
        # template = loader.get_template("initialization/first_run.html")
        # return HttpResponse(template.render({}, request))

    # If a base URL is set, redirect the user to it
    if request.path[1:] != BASE_URL:
        return redirect("/" + BASE_URL)

    return homepage(request)


@cache_page(1)
@login_required
def homepage(request):
    # Generate the base template
    template = loader.get_template("primary/base.html")
    context = generate_context({})
    return HttpResponse(template.render(context, request))
