# from django.shortcuts import render
from threading import Thread

from conreq import content_discovery, searcher
from conreq.apps.helpers import set_multi_conreq_status, generate_context
from django.http import HttpResponse
from django.template import loader


def convert_card_to_tmdb(index, all_results):
    # Convert Sonarr cards to TMDB
    if all_results[index].__contains__("tvdbId"):
        try:
            tmdb_query = content_discovery.get_by_tvdb_id(all_results[index]["tvdbId"])
            tmdb_result = tmdb_query["tv_results"][0]
            all_results[index] = tmdb_result
            all_results[index]["tmdbCard"] = True
        except:
            pass


# Create your views here.
def search(request):
    # Get the ID from the URL
    query = request.GET.get("query", "")
    content_type = request.GET.get("content_type", None)
    template = loader.get_template("search.html")

    # Determine which search method to use (tv/movie/all)
    if content_type == "tv":
        arr_results = searcher.television(query)
    elif content_type == "movie":
        arr_results = searcher.movie(query)
    else:
        arr_results = searcher.all(query)

    # Attempt to convert cards to TMDB equivalents
    thread_list = []
    for index in range(0, len(arr_results)):
        thread = Thread(target=convert_card_to_tmdb, args=[index, arr_results])
        thread.start()
        thread_list.append(thread)

    # Wait for computation to complete
    for thread in thread_list:
        thread.join()

    # Generate conreq status
    set_multi_conreq_status(arr_results)

    context = generate_context(
        {
            "all_cards": arr_results,
        }
    )
    return HttpResponse(template.render(context, request))
