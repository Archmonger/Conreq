# from django.shortcuts import render
from conreq import content_discovery
from conreq.apps.helpers import generate_context, set_many_conreq_status
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader


# Create your views here.
@login_required
def discover_all(request):
    template = loader.get_template("viewport/discover.html")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Search for TV content
    tmdb_results = content_discovery.all(page, page_multiplier=2)["results"]

    # Set conreq status for all cards
    set_many_conreq_status(tmdb_results)

    context = generate_context(
        {
            "all_cards": tmdb_results,
        }
    )

    return HttpResponse(template.render(context, request))


@login_required
def discover_tv(request):
    template = loader.get_template("viewport/discover.html")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Search for TV content
    tmdb_results = content_discovery.tv(page, page_multiplier=2)["results"]

    # Set conreq status for all cards
    set_many_conreq_status(tmdb_results)

    context = generate_context(
        {
            "all_cards": tmdb_results,
        }
    )

    return HttpResponse(template.render(context, request))


@login_required
def discover_movies(request):
    template = loader.get_template("viewport/discover.html")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Search for TV content
    tmdb_results = content_discovery.movies(page, page_multiplier=2)["results"]

    # Set conreq status for all cards
    set_many_conreq_status(tmdb_results)

    context = generate_context(
        {
            "all_cards": tmdb_results,
        }
    )

    return HttpResponse(template.render(context, request))
