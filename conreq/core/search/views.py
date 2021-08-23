from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page

from conreq.core.discover.helpers import set_many_availability
from conreq.core.tmdb.discovery import TmdbDiscovery
from conreq.core.tmdb.search import TmdbSearch
from conreq.utils.debug import performance_metrics


@cache_page(15)
@login_required
@performance_metrics()
def search(request):
    content_discovery = TmdbDiscovery()
    searcher = TmdbSearch()

    # Get the ID from the URL
    query = request.GET.get("query", "")
    content_type = request.GET.get("content_type", None)
    page = int(request.GET.get("page", 1))

    # Determine which search method to use (tv/movie/all)
    if content_type == "tv":
        tmdb_results = searcher.television(query, page)
    elif content_type == "movie":
        tmdb_results = searcher.movie(query, page)
    else:
        tmdb_results = searcher.all(query, page)

    if tmdb_results:
        tmdb_results = tmdb_results.get("results")

        # Determine the availability
        content_discovery.determine_id_validity(tmdb_results)
        set_many_availability(tmdb_results)

    context = {
        "all_cards": tmdb_results,
        "content_type": content_type,
        "search_query": query,
    }
    template = loader.get_template("viewport/search.html")
    return HttpResponse(template.render(context, request))
