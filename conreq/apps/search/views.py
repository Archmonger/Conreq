# from django.shortcuts import render
from threading import Thread

from conreq import content_discovery, searcher
from conreq.apps_helper import generate_context, obtain_conreq_status
from django.http import HttpResponse
from django.template import loader


def convert_cards_to_tmdb(index, all_results):
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
    arr_results = searcher.all(query)
    template = loader.get_template("search.html")

    # Attempt to convert cards to TMDB equivalents
    thread_list = []
    for index in range(0, len(arr_results)):
        thread = Thread(target=convert_cards_to_tmdb, args=[index, arr_results])
        thread.start()
        thread_list.append(thread)

    # Wait for computation to complete
    for thread in thread_list:
        thread.join()

    context = generate_context(
        {
            "all_cards": arr_results,
        }
    )
    return HttpResponse(template.render(context, request))
