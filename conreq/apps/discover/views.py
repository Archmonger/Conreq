# from django.shortcuts import render
from conreq.utils.apps import generate_context, set_many_conreq_status
from conreq.core.content_discovery import ContentDiscovery
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

# Create your views here.
@login_required
def discover_all(request):
    content_discovery = ContentDiscovery()
    template = loader.get_template("viewport/discover.html")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Search for TV content
    tmdb_results = content_discovery.all(page)["results"]

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
    content_discovery = ContentDiscovery()
    template = loader.get_template("viewport/discover.html")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Search for TV content
    tmdb_results = content_discovery.tv(page)["results"]

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
    content_discovery = ContentDiscovery()
    template = loader.get_template("viewport/discover.html")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Search for TV content
    tmdb_results = content_discovery.movies(page)["results"]

    # Set conreq status for all cards
    set_many_conreq_status(tmdb_results)

    context = generate_context(
        {
            "all_cards": tmdb_results,
        }
    )

    return HttpResponse(template.render(context, request))
