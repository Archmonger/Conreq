from conreq.core.content_discovery.tmdb import ContentDiscovery
from conreq.core.content_search import Search
from conreq.utils.app_views import set_many_availability
from conreq.utils.testing import performance_metrics
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page


@cache_page(15)
@login_required
@performance_metrics()
def search(request):
    content_discovery = ContentDiscovery()
    searcher = Search()

    # Get the ID from the URL
    query = request.GET.get("query", "")
    content_type = request.GET.get("content_type", None)
    page = int(request.GET.get("page", 1))

    # Determine which search method to use (tv/movie/all)
    if content_type == "tv":
        tmdb_results = searcher.television(query, page)["results"]
    elif content_type == "movie":
        tmdb_results = searcher.movie(query, page)["results"]
    else:
        tmdb_results = searcher.all(query, page)["results"]

    # Determine the availability
    content_discovery.determine_id_validity({"results": tmdb_results})
    set_many_availability(tmdb_results)

    context = {
        "all_cards": tmdb_results,
        "content_type": content_type,
        "search_query": query,
    }
    template = loader.get_template("viewport/search.html")
    return HttpResponse(template.render(context, request))
