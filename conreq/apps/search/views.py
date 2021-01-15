# from django.shortcuts import render
from threading import Thread

from conreq.bootup import content_discovery, searcher
from conreq.apps.helpers import (
    convert_card_to_tmdb,
    generate_context,
    set_many_conreq_status,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader


# Create your views here.
@login_required
def search(request):
    # Get the ID from the URL
    query = request.GET.get("query", "")
    content_type = request.GET.get("content_type", None)
    template = loader.get_template("viewport/search.html")

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
    content_discovery.determine_id_validity({"results": arr_results})
    set_many_conreq_status(arr_results)

    context = generate_context(
        {
            "all_cards": arr_results,
        }
    )
    return HttpResponse(template.render(context, request))
