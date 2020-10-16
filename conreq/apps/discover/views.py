# from django.shortcuts import render
from threading import Thread

from django.http import HttpResponse
from django.template import loader
from conreq import content_discovery
from conreq.apps_helper import obtain_conreq_status, generate_context


# Create your views here.
def discover(request, page=1):

    # Get the ID from the URL
    content_type = request.GET.get("content_type", None)

    if content_type == "tv":
        tmdb_results = content_discovery.tv(page)["results"]
        active_tab = "TV Shows"

    elif content_type == "movies":
        tmdb_results = content_discovery.movies(page)["results"]
        active_tab = "Movies"

    else:
        tmdb_results = content_discovery.all(page)["results"]
        active_tab = "Discover"

    template = loader.get_template("discover.html")

    thread_list = []
    for card in tmdb_results:
        thread = Thread(target=obtain_conreq_status, args=[card])
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    context = generate_context(
        {
            "all_cards": tmdb_results,
            "active_tab": active_tab,
        }
    )
    return HttpResponse(template.render(context, request))
