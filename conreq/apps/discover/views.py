from conreq.core.content_discovery import ContentDiscovery
from conreq.utils.apps import generate_context, set_many_availability
from conreq.utils.testing import performance_metrics
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page


@cache_page(60)
@login_required
@performance_metrics()
def discover_all(request):
    content_discovery = ContentDiscovery()
    template = loader.get_template("viewport/discover.html")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Search for TV content
    tmdb_results = content_discovery.all(page)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = generate_context(
        {
            "all_cards": tmdb_results,
        }
    )

    return HttpResponse(template.render(context, request))


@cache_page(60)
@login_required
@performance_metrics()
def discover_tv(request):
    content_discovery = ContentDiscovery()
    template = loader.get_template("viewport/discover.html")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Search for TV content
    tmdb_results = content_discovery.tv(page, page_multiplier=2)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = generate_context(
        {
            "all_cards": tmdb_results,
        }
    )

    return HttpResponse(template.render(context, request))


@cache_page(60)
@login_required
@performance_metrics()
def discover_movies(request):
    content_discovery = ContentDiscovery()
    template = loader.get_template("viewport/discover.html")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Search for TV content
    tmdb_results = content_discovery.movies(page, page_multiplier=2)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = generate_context(
        {
            "all_cards": tmdb_results,
        }
    )

    return HttpResponse(template.render(context, request))
