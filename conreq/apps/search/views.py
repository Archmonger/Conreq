# from django.shortcuts import render
from threading import Thread

from django.http import HttpResponse
from django.template import loader
from conreq import content_discovery, searcher
from conreq.apps_helper import obtain_conreq_status, generate_context


# Create your views here.
def search(request):

    # Get the ID from the URL
    query = request.GET.get("query", "")
    arr_results = searcher.all(query)
    template = loader.get_template("search.html")

    context = generate_context(
        {
            "all_cards": arr_results,
        }
    )
    return HttpResponse(template.render(context, request))
