from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.views.decorators.cache import cache_page
from titlecase import titlecase

from conreq.core.discover.helpers import set_many_availability
from conreq.core.tmdb.discovery import TmdbDiscovery
from conreq.core.tmdb.preset_filters import combined_filters, movie_filters, tv_filters
from conreq.utils.debug import performance_metrics

from .helpers import preset_filter_extras


@cache_page(15)
@login_required
@performance_metrics()
def discover_all(request):
    content_discovery = TmdbDiscovery()
    discover_filter = request.GET.get("filter", "")
    filter_name = titlecase(discover_filter.replace("-", " "))
    page = int(request.GET.get("page", 1))

    # Get content
    filter_params = {}
    if discover_filter == "custom":
        filter_params = request.GET.dict()
        filter_params.pop("filter")
    if discover_filter:
        add_values = preset_filter_extras(request)
        tmdb_results = content_discovery.discover_by_filter(
            filter_name=discover_filter,
            page_number=page,
            add_values=add_values,
            **filter_params,
        )["results"]
    else:
        tmdb_results = content_discovery.all(page)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = {
        "all_cards": tmdb_results,
        "page_name": "TV & Movies",
        "filter_name": filter_name,
    }
    template = loader.get_template("viewport/discover.html")
    return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def discover_tv(request):
    content_discovery = TmdbDiscovery()
    discover_filter = request.GET.get("filter", "")
    filter_name = titlecase(discover_filter.replace("-", " "))
    page = int(request.GET.get("page", 1))

    # Get content
    filter_params = {}
    if discover_filter == "custom":
        filter_params = request.GET.dict()
        filter_params.pop("filter")
    if discover_filter:
        add_values = preset_filter_extras(request)
        tmdb_results = content_discovery.discover_tv_by_filter(
            filter_name=discover_filter,
            page_number=page,
            add_values=add_values,
            **filter_params,
        )["results"]
    else:
        tmdb_results = content_discovery.tv(page)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = {
        "all_cards": tmdb_results,
        "content_type": "tv",
        "page_name": "Television",
        "filter_name": filter_name,
    }
    template = loader.get_template("viewport/discover.html")
    return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def discover_movies(request):
    content_discovery = TmdbDiscovery()
    discover_filter = request.GET.get("filter", "")
    filter_name = titlecase(discover_filter.replace("-", " "))
    page = int(request.GET.get("page", 1))

    # Get content
    filter_params = {}
    if discover_filter == "custom":
        filter_params = request.GET.dict()
        filter_params.pop("filter")
    if discover_filter:
        add_values = preset_filter_extras(request)
        tmdb_results = content_discovery.discover_movie_by_filter(
            filter_name=discover_filter,
            page_number=page,
            add_values=add_values,
            **filter_params,
        )["results"]
    else:
        tmdb_results = content_discovery.movies(page)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = {
        "all_cards": tmdb_results,
        "content_type": "movie",
        "page_name": "Movies",
        "filter_name": filter_name,
    }
    template = loader.get_template("viewport/discover.html")
    return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def simple_filter_modal(request):
    content_type = request.GET.get("content_type")
    if content_type == "tv":
        filters = tv_filters().keys()
        filter_url = reverse("discover:tv")
    elif content_type == "movie":
        filters = movie_filters().keys()
        filter_url = reverse("discover:movies")
    else:
        filters = combined_filters().keys()
        filter_url = reverse("discover:all")
    context = {
        "content_type": content_type,
        "filters": filters,
        "filter_url": filter_url,
    }
    template = loader.get_template("modal/discover_filter_simple.html")
    return HttpResponse(template.render(context, request))
