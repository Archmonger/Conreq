"""Helpers for More Info"""
import re
from calendar import month_name
from io import StringIO

from markdown import Markdown

TMDB_BACKDROP_URL = "https://image.tmdb.org/t/p/original"
TMDB_POSTER_URL = "https://image.tmdb.org/t/p/w500"


def __strip_urls(text):
    """Removes all URLs from a string"""
    return re.sub(r"^https?:\/\/.*[\r\n]*", "", text, flags=re.MULTILINE)


def __strip_html(html):
    """Removes HTML from a string."""
    return re.sub("<[^<]+?>", "", html)


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


def preprocess_tmdb_result(tmdb_result):
    """Pre-processing to allow for viewing within the More Info screen."""
    # Prepare data attributes for the HTML
    # Summary
    if (
        tmdb_result.__contains__("overview")
        and isinstance(tmdb_result["overview"], str)
        and not tmdb_result["overview"]
    ):
        tmdb_result["overview"] = None
    # Budget
    if tmdb_result.__contains__("budget") and isinstance(tmdb_result["budget"], int):
        tmdb_result["budget"] = (
            "{:,}".format(tmdb_result["budget"])
            if tmdb_result["budget"]
            else None
        )
    # Revenue
    if tmdb_result.__contains__("revenue") and isinstance(tmdb_result["revenue"], int):
        tmdb_result["revenue"] = (
            "{:,}".format(tmdb_result["revenue"])
            if tmdb_result["revenue"]
            else None
        )
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
        if not tmdb_result["reviews"]["results"]:
            tmdb_result["reviews"]["results"] = None
        else:
            for review in tmdb_result["reviews"]["results"]:
                review["content"] = __strip_urls(
                    __strip_html(__md.convert(review["content"]))
                )
    # Keywords (Tags)
    if (
        tmdb_result.__contains__("keywords")
        and tmdb_result["keywords"].__contains__("results")
        and isinstance(tmdb_result["keywords"]["results"], list)
        and not tmdb_result["keywords"]["results"]
    ):
        tmdb_result["keywords"]["results"] = None
    # Cast Members
    if (
        tmdb_result.__contains__("credits")
        and tmdb_result["credits"].__contains__("cast")
        and isinstance(tmdb_result["credits"]["cast"], list)
        and not tmdb_result["credits"]["cast"]
    ):
        tmdb_result["credits"]["cast"] = None
    # Videos
    if (
        tmdb_result.__contains__("videos")
        and tmdb_result["videos"].__contains__("results")
        and isinstance(tmdb_result["videos"]["results"], list)
    ):
        if not tmdb_result["videos"]["results"]:
            tmdb_result["videos"]["results"] = None
        else:
            contains_youtube = any(
                video["site"] == "YouTube"
                for video in tmdb_result["videos"]["results"]
            )
            if not contains_youtube:
                tmdb_result["videos"]["results"] = None
    # Artwork (Images)
    if (
        tmdb_result.__contains__("images")
        and tmdb_result["images"].__contains__("backdrops")
        and isinstance(tmdb_result["images"]["backdrops"], list)
        and not tmdb_result["images"]["backdrops"]
    ):
        tmdb_result["images"]["backdrops"] = None
    # Last Air Date
    if (
        tmdb_result.__contains__("last_air_date")
        and isinstance(tmdb_result["last_air_date"], str)
        and tmdb_result["last_air_date"]
    ):
        year, month, day = tmdb_result["last_air_date"].split(sep="-")
        month = month_name[int(month)]
        tmdb_result["last_air_date_formatted"] = f"{month} {day}, {year}"
    # First Air Date
    if (
        tmdb_result.__contains__("first_air_date")
        and isinstance(tmdb_result["first_air_date"], str)
        and tmdb_result["first_air_date"]
    ):
        year, month, day = tmdb_result["first_air_date"].split(sep="-")
        month = month_name[int(month)]
        tmdb_result["first_air_date_formatted"] = f"{month} {day}, {year}"
    # Next Air Date
    if tmdb_result.get("next_episode_to_air") and tmdb_result[
        "next_episode_to_air"
    ].get("air_date"):
        year, month, day = tmdb_result["next_episode_to_air"]["air_date"].split(sep="-")
        month = month_name[int(month)]
        tmdb_result["next_air_date_formatted"] = f"{month} {day}, {year}"
    # Release Date
    if (
        tmdb_result.__contains__("release_date")
        and isinstance(tmdb_result["release_date"], str)
        and tmdb_result["release_date"]
    ):
        year, month, day = tmdb_result["release_date"].split(sep="-")
        month = month_name[int(month)]
        tmdb_result["release_date_formatted"] = f"{month} {day}, {year}"
    # Backdrop
    if (
        tmdb_result.__contains__("backdrop_path")
        and isinstance(tmdb_result["backdrop_path"], str)
        and tmdb_result["backdrop_path"]
        and tmdb_result["backdrop_path"].find(TMDB_BACKDROP_URL) == -1
    ):
        tmdb_result["backdrop_path"] = TMDB_BACKDROP_URL + tmdb_result["backdrop_path"]
    # Poster
    if (
        tmdb_result.__contains__("poster_path")
        and isinstance(tmdb_result["poster_path"], str)
        and tmdb_result["poster_path"]
        and tmdb_result["poster_path"].find(TMDB_POSTER_URL) == -1
    ):
        tmdb_result["poster_path"] = TMDB_POSTER_URL + tmdb_result["poster_path"]


def preprocess_tmdb_person(tmdb_result):
    """Pre-processing to allow for viewing within the More Info screen."""
    # Prepare data attributes for the HTML
    # Birthday
    if (
        tmdb_result.__contains__("birthday")
        and isinstance(tmdb_result["birthday"], str)
        and tmdb_result["birthday"]
    ):
        year, month, day = tmdb_result["birthday"].split(sep="-")
        month = month_name[int(month)]
        tmdb_result["birthday_formatted"] = f"{month} {day}, {year}"
    # Deathday
    if (
        tmdb_result.__contains__("deathday")
        and isinstance(tmdb_result["deathday"], str)
        and tmdb_result["deathday"]
    ):
        year, month, day = tmdb_result["deathday"].split(sep="-")
        month = month_name[int(month)]
        tmdb_result["deathday_formatted"] = f"{month} {day}, {year}"
    # Poster
    if (
        tmdb_result.__contains__("profile_path")
        and isinstance(tmdb_result["profile_path"], str)
        and tmdb_result["profile_path"]
        and tmdb_result["profile_path"].find(TMDB_POSTER_URL) == -1
    ):
        tmdb_result["profile_path"] = TMDB_POSTER_URL + tmdb_result["profile_path"]
