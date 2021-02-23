"""Helpers for More Info"""
from calendar import month_name
from io import StringIO

from conreq.utils.generic import is_key_value_in_list
from markdown import Markdown

TMDB_BACKDROP_URL = "https://image.tmdb.org/t/p/original"
TMDB_POSTER_300_URL = "https://image.tmdb.org/t/p/w300"

# Helper to remove markdown from string
def __unmark_element(element, stream=None):
    """Processing function to removes markdown from an element."""
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        __unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# Patching the markdown module to remove markdown
Markdown.output_formats["plain"] = __unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def preprocess_arr_result(arr_result):
    """Pre-processing to allow for viewing within the More Info screen."""
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
            "coverType", "fanart", arr_result["images"], return_item=True
        )
        if backdrop is not False:
            arr_result["backdropPath"] = backdrop["url"]


def preprocess_tmdb_result(tmdb_result):
    """Pre-processing to allow for viewing within the More Info screen."""
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
                review["content"] = __md.convert(review["content"])
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
    ):
        if len(tmdb_result["videos"]["results"]) == 0:
            tmdb_result["videos"]["results"] = None
        else:
            contains_youtube = False
            for video in tmdb_result["videos"]["results"]:
                if video["site"] == "YouTube":
                    contains_youtube = True
                    break
            if not contains_youtube:
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
    # First Air Date
    if (
        tmdb_result.__contains__("first_air_date")
        and isinstance(tmdb_result["first_air_date"], str)
        and len(tmdb_result["first_air_date"]) != 0
    ):
        year, month, day = tmdb_result["first_air_date"].split(sep="-")
        month = month_name[int(month)]
        tmdb_result["first_air_date_formatted"] = f"{month} {day}, {year}"
    # Next Air Date
    if (
        tmdb_result.__contains__("next_episode_to_air")
        and isinstance(tmdb_result["next_episode_to_air"], dict)
        and tmdb_result["next_episode_to_air"]
        and tmdb_result["next_episode_to_air"].__contains__("air_date")
        and isinstance(tmdb_result["next_episode_to_air"]["air_date"], str)
        and tmdb_result["next_episode_to_air"]["air_date"]
    ):
        year, month, day = tmdb_result["next_episode_to_air"]["air_date"].split(sep="-")
        month = month_name[int(month)]
        tmdb_result["next_air_date_formatted"] = f"{month} {day}, {year}"
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
