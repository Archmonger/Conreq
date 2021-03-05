from conreq.core.content_discovery.tmdb import ContentDiscovery
from conreq.core.content_discovery.tmdb_preset_filters import (
    combined_filters,
    movie_filters,
    tv_filters,
)
from conreq.utils.app_views import set_many_availability
from conreq.utils.testing import performance_metrics
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page


@cache_page(15)
@login_required
@performance_metrics()
def discover_all(request):
    content_discovery = ContentDiscovery()
    template = loader.get_template("viewport/discover.html")
    preset_filter = request.GET.get("filter", "")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Get content
    if preset_filter:
        tmdb_results = content_discovery.discover_by_preset_filter(
            preset_filter, page, page_multiplier=2
        )["results"]
    else:
        tmdb_results = content_discovery.all(page)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = {
        "all_cards": tmdb_results,
    }

    return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def discover_tv(request):
    content_discovery = ContentDiscovery()
    preset_filter = request.GET.get("filter", "")
    page = int(request.GET.get("page", 1))

    # Get content
    if preset_filter:
        tmdb_results = content_discovery.discover_tv_by_preset_filter(
            preset_filter, page, page_multiplier=2
        )["results"]
    else:
        tmdb_results = content_discovery.tv(page, page_multiplier=2)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = {"all_cards": tmdb_results}
    template = loader.get_template("viewport/discover.html")
    return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def discover_movies(request):
    content_discovery = ContentDiscovery()
    preset_filter = request.GET.get("filter", "")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Get content
    if preset_filter:
        tmdb_results = content_discovery.discover_movie_by_preset_filter(
            preset_filter, page, page_multiplier=2
        )["results"]
    else:
        tmdb_results = content_discovery.movies(page, page_multiplier=2)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = {"all_cards": tmdb_results}
    template = loader.get_template("viewport/discover.html")
    return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def simple_filter_modal(request):
    template = loader.get_template("modal/discover_filter_simple.html")
    content_type = request.GET.get("content_type")
    context = {
        "content_type": content_type,
        "tv_filters": tv_filters().keys(),
        "movie_filters": movie_filters().keys(),
        "combined_filters": combined_filters().keys(),
    }
    return HttpResponse(template.render(context, request))
