from calendar import month_name
from threading import Thread

from conreq import content_discovery, searcher
from conreq.apps_helper import (
    TMDB_BACKDROP_URL,
    TMDB_POSTER_300_URL,
    arr_conreq_status,
    generate_context,
    tmdb_conreq_status,
)
from conreq.core.generic_tools import is_key_value_in_list
from conreq.core.thread_helper import ReturnThread
from django.http import HttpResponse
from django.template import loader


def preprocess_arr_result(arr_result):
    # Prepare data attributes for the HTML
    # Summary
    if (
        arr_result.__contains__("overview")
        and isinstance(arr_result["overview"], str)
        and len(arr_result["overview"]) == 0
    ):
        arr_result["overview"] = None
    # Runtime
    if arr_result.__contains__("runtime") and isinstance(arr_result["runtime"], int):
        arr_result["runtime"] = "{:d}h {:d}m".format(*divmod(arr_result["runtime"], 60))
    # Release Status
    if arr_result.__contains__("status") and isinstance(arr_result["status"], str):
        if len(arr_result["status"]) == 0:
            arr_result["status"] = None
        else:
            arr_result["status"] = arr_result["status"].capitalize()
    # Genres
    if (
        arr_result.__contains__("genres")
        and isinstance(arr_result["genres"], list)
        and len(arr_result["genres"]) == 0
    ):
        arr_result["genres"] = None
    # Networks
    if (
        arr_result.__contains__("network")
        and isinstance(arr_result["network"], list)
        and len(arr_result["network"]) != 0
    ):
        arr_result["networks"] = arr_result["network"]
    if (
        arr_result.__contains__("network")
        and isinstance(arr_result["network"], str)
        and len(arr_result["network"]) != 0
    ):
        arr_result["networks"] = [arr_result["network"]]
    # Backdrop
    if (
        arr_result.__contains__("images")
        and isinstance(arr_result["images"], list)
        and len(arr_result["images"]) != 0
    ):
        backdrop = is_key_value_in_list(
            arr_result["images"], "coverType", "fanart", return_item=True
        )
        if backdrop is not None:
            arr_result["backdropPath"] = backdrop["url"]


def preprocess_tmdb_result(tmdb_result):
    # Prepare data attributes for the HTML
    # Summary
    if (
        tmdb_result.__contains__("overview")
        and isinstance(tmdb_result["overview"], str)
        and len(tmdb_result["overview"]) == 0
    ):
        tmdb_result["overview"] = None
    # Budget
    if tmdb_result.__contains__("budget") and isinstance(tmdb_result["budget"], int):
        if tmdb_result["budget"] == 0:
            tmdb_result["budget"] = None
        else:
            tmdb_result["budget"] = "{:,}".format(tmdb_result["budget"])
    # Revenue
    if tmdb_result.__contains__("revenue") and isinstance(tmdb_result["revenue"], int):
        if tmdb_result["revenue"] == 0:
            tmdb_result["revenue"] = None
        else:
            tmdb_result["revenue"] = "{:,}".format(tmdb_result["revenue"])
    # Runtime
    if tmdb_result.__contains__("runtime") and isinstance(tmdb_result["runtime"], int):
        tmdb_result["runtime"] = "{:d}h {:d}m".format(
            *divmod(tmdb_result["runtime"], 60)
        )
    # Reviews
    if (
        tmdb_result.__contains__("reviews")
        and tmdb_result["reviews"].__contains__("results")
        and isinstance(tmdb_result["reviews"]["results"], list)
    ):
        if len(tmdb_result["reviews"]["results"]) == 0:
            tmdb_result["reviews"]["results"] = None
        else:
            for review in tmdb_result["reviews"]["results"]:
                if len(review["content"]) > 400:
                    review["content"] = review["content"][:400] + "..."
    # Keywords (Tags)
    if (
        tmdb_result.__contains__("keywords")
        and tmdb_result["keywords"].__contains__("results")
        and isinstance(tmdb_result["keywords"]["results"], list)
        and len(tmdb_result["keywords"]["results"]) == 0
    ):
        tmdb_result["keywords"]["results"] = None
    # Cast Members
    if (
        tmdb_result.__contains__("credits")
        and tmdb_result["credits"].__contains__("cast")
        and isinstance(tmdb_result["credits"]["cast"], list)
        and len(tmdb_result["credits"]["cast"]) == 0
    ):
        tmdb_result["credits"]["cast"] = None
    # Videos
    if (
        tmdb_result.__contains__("videos")
        and tmdb_result["videos"].__contains__("results")
        and isinstance(tmdb_result["videos"]["results"], list)
        and len(tmdb_result["videos"]["results"]) == 0
    ):
        tmdb_result["videos"]["results"] = None
    # Artwork (Images)
    if (
        tmdb_result.__contains__("images")
        and tmdb_result["images"].__contains__("backdrops")
        and isinstance(tmdb_result["images"]["backdrops"], list)
        and len(tmdb_result["images"]["backdrops"]) == 0
    ):
        tmdb_result["images"]["backdrops"] = None
    # Last Air Date
    if (
        tmdb_result.__contains__("last_air_date")
        and isinstance(tmdb_result["last_air_date"], str)
        and len(tmdb_result["last_air_date"]) != 0
    ):
        year, month, day = tmdb_result["last_air_date"].split(sep="-")
        month = month_name[int(month)]
        tmdb_result["last_air_date_formatted"] = f"{month} {day}, {year}"
    # Release Date
    if (
        tmdb_result.__contains__("release_date")
        and isinstance(tmdb_result["release_date"], str)
        and len(tmdb_result["release_date"]) != 0
    ):
        year, month, day = tmdb_result["release_date"].split(sep="-")
        month = month_name[int(month)]
        tmdb_result["release_date_formatted"] = f"{month} {day}, {year}"
    # Backdrop
    if (
        tmdb_result.__contains__("backdrop_path")
        and isinstance(tmdb_result["backdrop_path"], str)
        and len(tmdb_result["backdrop_path"]) != 0
        and tmdb_result["backdrop_path"].find(TMDB_BACKDROP_URL) == -1
    ):
        tmdb_result["backdrop_path"] = TMDB_BACKDROP_URL + tmdb_result["backdrop_path"]
    # Poster
    if (
        tmdb_result.__contains__("poster_path")
        and isinstance(tmdb_result["poster_path"], str)
        and len(tmdb_result["poster_path"]) != 0
        and tmdb_result["poster_path"].find(TMDB_POSTER_300_URL) == -1
    ):
        tmdb_result["poster_path"] = TMDB_POSTER_300_URL + tmdb_result["poster_path"]
    # Content Type
    if tmdb_result.__contains__("name"):
        tmdb_result["content_type"] = "tv"
    elif tmdb_result.__contains__("title"):
        tmdb_result["content_type"] = "movie"


# Create your views here.
def more_info(request):
    template = loader.get_template("more-info.html")
    thread_list = []

    # Get the ID from the URL
    tmdb_id = request.GET.get("tmdb_id", None)
    tvdb_id = request.GET.get("tvdb_id", None)

    if tmdb_id is not None:
        content_type = request.GET.get("content_type", None)

        # Get all the basic metadata for a given ID
        tmdb_result = content_discovery.get_by_tmdb_id(tmdb_id, content_type)

        # Get recommended results
        similar_and_recommended_thread = ReturnThread(
            target=content_discovery.similar_and_recommended,
            args=[tmdb_id, content_type],
        )
        similar_and_recommended_thread.start()

        # Checking Conreq status of the current TMDB ID
        thread = Thread(target=tmdb_conreq_status, args=[tmdb_result])
        thread.start()
        thread_list.append(thread)

        # Pre-parse data attributes within tmdb_result
        thread = Thread(target=preprocess_tmdb_result, args=[tmdb_result])
        thread.start()
        thread_list.append(thread)

        # Get collection information
        if (
            tmdb_result.__contains__("belongs_to_collection")
            and tmdb_result["belongs_to_collection"] is not None
        ):
            tmdb_collection = True
            tmdb_collection_thread = ReturnThread(
                target=content_discovery.collections,
                args=[tmdb_result["belongs_to_collection"]["id"]],
            )
            tmdb_collection_thread.start()
        else:
            tmdb_collection = None

        # Checking Conreq status for all recommended content
        tmdb_recommended = similar_and_recommended_thread.join()
        # Recommended Content
        if isinstance(tmdb_recommended, list) and len(tmdb_recommended) == 0:
            tmdb_recommended = None
        for card in tmdb_recommended["results"]:
            thread = Thread(target=tmdb_conreq_status, args=[card])
            thread.start()
            thread_list.append(thread)

        # Wait for thread computation to complete
        for thread in thread_list:
            thread.join()
        if tmdb_collection is not None:
            tmdb_collection = tmdb_collection_thread.join()

        # Generate context for page rendering
        context = generate_context(
            {
                "content": tmdb_result,
                "recommended": tmdb_recommended,
                "collection": tmdb_collection,
                "content_type": tmdb_result["content_type"],
            }
        )

    elif tvdb_id is not None:
        # Fallback for TVDB
        arr_result = searcher.television(tvdb_id)[0]
        preprocess_arr_result(arr_result)
        arr_conreq_status(arr_result)

        # Generate context for page rendering
        context = generate_context(
            {
                "content": arr_result,
                "content_type": arr_result["contentType"],
            }
        )

    # Render the page
    return HttpResponse(template.render(context, request))
