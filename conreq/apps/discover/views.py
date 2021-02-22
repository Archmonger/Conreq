from conreq.core.content_discovery.tmdb import ContentDiscovery
from conreq.utils.app_views import generate_context, set_many_availability
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
    simple_filter = request.GET.get("filter")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Get content
    if simple_filter == "popular":
        tmdb_results = content_discovery.popular(page)["results"]
    elif simple_filter == "top":
        tmdb_results = content_discovery.top(page)["results"]
    else:
        tmdb_results = content_discovery.all(page)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = generate_context(
        {
            "all_cards": tmdb_results,
        }
    )

    return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def discover_tv(request):
    content_discovery = ContentDiscovery()
    template = loader.get_template("viewport/discover.html")
    simple_filter = request.GET.get("filter")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Get content
    if simple_filter == "popular":
        tmdb_results = content_discovery.popular_tv(page, page_multiplier=2)["results"]
    elif simple_filter == "top":
        tmdb_results = content_discovery.top_tv(page, page_multiplier=2)["results"]
    elif simple_filter == "airing":
        tmdb_results = content_discovery.on_the_air_tv(page, page_multiplier=2)[
            "results"
        ]
    elif simple_filter == "today":
        tmdb_results = content_discovery.airing_today_tv(page, page_multiplier=2)[
            "results"
        ]
    else:
        tmdb_results = content_discovery.tv(page, page_multiplier=2)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = generate_context(
        {
            "all_cards": tmdb_results,
        }
    )

    return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def discover_movies(request):
    content_discovery = ContentDiscovery()
    template = loader.get_template("viewport/discover.html")
    simple_filter = request.GET.get("filter")

    # Get the page number from the URL
    page = int(request.GET.get("page", 1))

    # Get content
    if simple_filter == "popular":
        tmdb_results = content_discovery.popular_movies(page, page_multiplier=2)[
            "results"
        ]
    elif simple_filter == "top":
        tmdb_results = content_discovery.top_movies(page, page_multiplier=2)["results"]
    else:
        tmdb_results = content_discovery.movies(page, page_multiplier=2)["results"]

    # Set the availability for all cards
    set_many_availability(tmdb_results)

    context = generate_context(
        {
            "all_cards": tmdb_results,
        }
    )

    return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def simple_filter_modal(request):
    template = loader.get_template("modal/discover_filter_simple.html")
    content_type = request.GET.get("content_type")
    context = {"content_type": content_type}
    return HttpResponse(template.render(context, request))