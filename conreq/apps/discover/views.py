# from django.shortcuts import render
from conreq import content_discovery
from conreq.apps.helpers import (
    STATIC_CONTEXT_VARS,
    generate_context,
    set_many_conreq_status,
)
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def discover(request, page=1):

    # Get the ID from the URL
    content_type = request.GET.get("content_type", None)

    # Search for TV content if requested
    if content_type == "tv":
        tmdb_results = content_discovery.tv(page)["results"]
        active_tab = STATIC_CONTEXT_VARS["tv_shows"]

    # Search for movie content if requested
    elif content_type == "movie":
        tmdb_results = content_discovery.movies(page)["results"]
        active_tab = STATIC_CONTEXT_VARS["movies"]

    # Search for both content if requested
    else:
        tmdb_results = content_discovery.all(page)["results"]
        active_tab = STATIC_CONTEXT_VARS["discover"]

    template = loader.get_template("discover.html")

    # Set conreq status for all cards
    set_many_conreq_status(tmdb_results)

    context = generate_context(
        {
            "all_cards": tmdb_results,
            "active_tab": active_tab,
        }
    )
    return HttpResponse(template.render(context, request))
