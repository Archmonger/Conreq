from conreq import content_discovery
from conreq.apps_helper import generate_context, tmdb_conreq_status
from django.http import HttpResponse
from django.template import loader
from threading import Thread
from calendar import month_name

# Create your views here.
def more_info(request):
    template = loader.get_template("more-info.html")

    # Get the ID from the URL
    tmdb_id = request.GET.get("tmdb_id", None)
    content_type = request.GET.get("content_type", None)

    # Get all the basic metadata for a given ID
    tmdb_object = content_discovery.get_by_tmdb_id(tmdb_id, content_type)

    # Get recommended results
    tmdb_recommended = content_discovery.similar_and_recommended(tmdb_id, content_type)[
        "results"
    ]

    # Get collection information
    if (
        tmdb_object.__contains__("belongs_to_collection")
        and tmdb_object["belongs_to_collection"] is not None
    ):
        tmdb_collection = content_discovery.collections(
            tmdb_object["belongs_to_collection"]["id"]
        )
    else:
        tmdb_collection = None

    # Check the availability in Sonarr/Radarr
    thread_list = []

    # Checking Conreq status of the current TMDB ID
    thread = Thread(target=tmdb_conreq_status, args=[tmdb_object])
    thread.start()
    thread_list.append(thread)

    # Checking Conreq status for all recommended content
    for card in tmdb_recommended:
        thread = Thread(target=tmdb_conreq_status, args=[card])
        thread.start()
        thread_list.append(thread)

    # Wait for thread computation to complete
    for thread in thread_list:
        thread.join()

    # Prepare data attributes for the HTML
    # Recommended Content
    if isinstance(tmdb_recommended, list) and len(tmdb_recommended) == 0:
        tmdb_recommended = None
    # Summary
    if tmdb_object.__contains__("overview") and isinstance(
        tmdb_object["overview"], str
    ):
        if len(tmdb_object["overview"]) == 0:
            tmdb_object["overview"] = None
    # Budget
    if tmdb_object.__contains__("budget") and isinstance(tmdb_object["budget"], int):
        if tmdb_object["budget"] == 0:
            tmdb_object["budget"] = None
        else:
            tmdb_object["budget"] = "{:,}".format(tmdb_object["budget"])
    # Revenue
    if tmdb_object.__contains__("revenue") and isinstance(tmdb_object["revenue"], int):
        if tmdb_object["revenue"] == 0:
            tmdb_object["revenue"] = None
        else:
            tmdb_object["revenue"] = "{:,}".format(tmdb_object["revenue"])
    # Runtime
    if tmdb_object.__contains__("runtime") and isinstance(tmdb_object["runtime"], int):
        tmdb_object["runtime"] = "{:d}h {:d}m".format(
            *divmod(tmdb_object["runtime"], 60)
        )
    # Reviews
    if (
        tmdb_object.__contains__("reviews")
        and tmdb_object["reviews"].__contains__("results")
        and isinstance(tmdb_object["reviews"]["results"], list)
    ):
        if len(tmdb_object["reviews"]["results"]) == 0:
            tmdb_object["reviews"]["results"] = None
        else:
            for review in tmdb_object["reviews"]["results"]:
                if len(review["content"]) > 400:
                    review["content"] = review["content"][:400] + "..."
    # Keywords (Tags)
    if (
        tmdb_object.__contains__("keywords")
        and tmdb_object["keywords"].__contains__("results")
        and isinstance(tmdb_object["keywords"]["results"], list)
        and len(tmdb_object["keywords"]["results"]) == 0
    ):
        tmdb_object["keywords"]["results"] = None
    # Cast Members
    if (
        tmdb_object.__contains__("credits")
        and tmdb_object["credits"].__contains__("cast")
        and isinstance(tmdb_object["credits"]["cast"], list)
        and len(tmdb_object["credits"]["cast"]) == 0
    ):
        tmdb_object["credits"]["cast"] = None
    # Videos
    if (
        tmdb_object.__contains__("videos")
        and tmdb_object["videos"].__contains__("results")
        and isinstance(tmdb_object["videos"]["results"], list)
        and len(tmdb_object["videos"]["results"]) == 0
    ):
        tmdb_object["videos"]["results"] = None
    # Artwork (Images)
    if (
        tmdb_object.__contains__("images")
        and tmdb_object["images"].__contains__("backdrops")
        and isinstance(tmdb_object["images"]["backdrops"], list)
        and len(tmdb_object["images"]["backdrops"]) == 0
    ):
        tmdb_object["images"]["backdrops"] = None
    # Last Air Date
    if (
        tmdb_object.__contains__("last_air_date")
        and isinstance(tmdb_object["last_air_date"], str)
        and len(tmdb_object["last_air_date"]) != 0
    ):
        year, month, day = tmdb_object["last_air_date"].split(sep="-")
        month = month_name[int(month)]
        tmdb_object["last_air_date"] = f"{month} {day}, {year}"
    # Release Date
    if (
        tmdb_object.__contains__("release_date")
        and isinstance(tmdb_object["release_date"], str)
        and len(tmdb_object["release_date"]) != 0
    ):
        year, month, day = tmdb_object["release_date"].split(sep="-")
        month = month_name[int(month)]
        tmdb_object["release_date"] = f"{month} {day}, {year}"

    # Render the page
    context = generate_context(
        {
            "content": tmdb_object,
            "recommended": tmdb_recommended,
            "collection": tmdb_collection,
        }
    )
    return HttpResponse(template.render(context, request))
