from calendar import month_name
from io import StringIO
from secrets import token_hex
from threading import Thread

from conreq.apps.server_settings.models import ConreqConfig
from conreq.apps.user_requests.models import UserRequest
from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.utils import cache, log
from conreq.utils.generic import is_key_value_in_list
from markdown import Markdown

__logger = log.get_logger(__name__)

TMDB_BACKDROP_URL = "https://image.tmdb.org/t/p/original"
TMDB_POSTER_300_URL = "https://image.tmdb.org/t/p/w300"

STATIC_CONTEXT_VARS = {
    "username": "username",
    "password": "password",
    "sign_in": "Sign In",
    "available": "Available",
    "partial": "Partial",
    "downloading": "Downloading",
    "discover": "Discover",
    "combined": "Combined",
    "tv_shows": "TV Shows",
    "movies": "Movies",
    "user_options": "User Options",
    "my_requests": "My Requests",
    "my_issues": "My Issues",
    "sign_out": "Sign Out",
    "admin": "Admin",
    "manage_users": "Manage Users",
    "email_users": "Email Users",
    "all_requests": "All Requests",
    "all_issues": "All Issues",
    "settings": "Settings",
    "server_settings": "Server Settings",
    "youtube": "YouTube",
}

# Helper to remove markdown from string
def __unmark_element(element, stream=None):
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


def generate_context(dict1):
    res = {**dict1, **STATIC_CONTEXT_VARS}
    return res


def __set_many_conreq_status(card, radarr_library, sonarr_library):
    # Sonarr card
    if card.__contains__("tvdbId"):
        if sonarr_library is not None and sonarr_library.__contains__(
            str(card["tvdbId"])
        ):
            card["conreqStatus"] = sonarr_library[str(card["tvdbId"])]["conreqStatus"]

    # Radarr card
    elif card.__contains__("tmdbId"):
        if radarr_library is not None and radarr_library.__contains__(
            str(card["tmdbId"])
        ):
            card["conreqStatus"] = radarr_library[str(card["tmdbId"])]["conreqStatus"]

    # TMDB TV card
    elif card.__contains__("name"):
        if (
            sonarr_library is not None
            and card.__contains__("tvdb_id")
            and sonarr_library.__contains__(str(card["tvdb_id"]))
        ):
            card["conreqStatus"] = sonarr_library[str(card["tvdb_id"])]["conreqStatus"]

    # TMDB movie card
    elif card.__contains__("title"):
        if radarr_library is not None and radarr_library.__contains__(str(card["id"])):
            card["conreqStatus"] = radarr_library[str(card["id"])]["conreqStatus"]


def set_many_conreq_status(results):
    content_manager = ContentManager()
    # Fetch Sonarr and Radarr libraries
    radarr_library = cache.handler(
        "radarr library cache",
        function=content_manager.get_all_radarr_content,
        cache_duration=70,
    )
    sonarr_library = cache.handler(
        "sonarr library cache",
        function=content_manager.get_all_sonarr_content,
        cache_duration=70,
    )

    # Generate conreq status if possible, or get the external ID if a TVDB ID is needed
    thread_list = []
    for card in results:
        thread = Thread(
            target=__set_many_conreq_status,
            args=[card, radarr_library, sonarr_library],
        )
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()

    return results


def set_single_conreq_status(card):
    content_manager = ContentManager()
    content_discovery = ContentDiscovery()
    try:
        # Compute conreq status of a Sonarr card
        if card.__contains__("tvdbId"):
            content = content_manager.get(tvdb_id=card["tvdbId"])
            if content is not None:
                card["conreqStatus"] = content["conreqStatus"]

        # Compute conreq status of a Radarr card
        elif card.__contains__("tmdbId"):
            content = content_manager.get(tmdb_id=card["tmdbId"])
            if content is not None:
                card["conreqStatus"] = content["conreqStatus"]

        # Compute conreq status of TV show
        elif card.__contains__("name"):
            external_id = content_discovery.get_external_ids(card["id"], "tv")
            content = content_manager.get(tvdb_id=external_id["tvdb_id"])
            if content is not None:
                card["conreqStatus"] = content["conreqStatus"]

        # Compute conreq status of movie
        elif card.__contains__("title"):
            content = content_manager.get(tmdb_id=card["id"])
            if content is not None:
                card["conreqStatus"] = content["conreqStatus"]

        # Something unexpected was passed in
        else:
            log.handler(
                "Card did not contain contentType, title, or name!",
                log.WARNING,
                __logger,
            )
            return card

    except:
        log.handler(
            "Could not determine Conreq Status of card!\n" + card,
            log.ERROR,
            __logger,
        )
        return card


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
            "coverType", "fanart", arr_result["images"], return_item=True
        )
        if backdrop is not False:
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


def convert_card_to_tmdb(index, all_results):
    content_discovery = ContentDiscovery()
    # NOTE: For some reason, overriding values in all_results requires the list and index value.
    # It will NOT work if attempting to change values by reference (ex. card = newCard).

    # Convert Sonarr cards to TMDB
    if all_results[index].__contains__("tvdbId"):
        try:
            tmdb_query = content_discovery.get_by_tvdb_id(all_results[index]["tvdbId"])
            tmdb_result = tmdb_query["tv_results"][0]
            all_results[index] = tmdb_result
            all_results[index]["tmdbCard"] = True
        except:
            pass


def obtain_sonarr_parameters(
    content_discovery,
    content_manager,
    tmdb_id=None,
    tvdb_id=None,
):
    """Returns the common parameters needed for adding a series to Sonarr."""
    conreq_config = ConreqConfig.get_solo()

    # Determine series type, root directory, and profile ID
    if tmdb_id is None:
        tmdb_id = content_discovery.get_by_tvdb_id(tvdb_id)["tv_results"]["id"]

    is_anime = content_discovery.is_anime(tmdb_id, "tv")
    season_folders = conreq_config.sonarr_season_folders
    all_root_dirs = content_manager.sonarr_root_dirs()

    if is_anime:
        series_type = "Anime"
        sonarr_root = is_key_value_in_list(
            "id", conreq_config.sonarr_anime_folder, all_root_dirs, return_item=True
        )["path"]
        sonarr_profile_id = conreq_config.sonarr_anime_quality_profile

    else:
        series_type = "Standard"
        sonarr_root = is_key_value_in_list(
            "id", conreq_config.sonarr_tv_folder, all_root_dirs, return_item=True
        )["path"]
        sonarr_profile_id = conreq_config.sonarr_tv_quality_profile

    return {
        "sonarr_profile_id": sonarr_profile_id,
        "sonarr_root": sonarr_root,
        "series_type": series_type,
        "season_folders": season_folders,
    }


def obtain_radarr_parameters(
    content_discovery,
    content_manager,
    tmdb_id=None,
):
    """Returns the common parameters needed for adding a series to Radarr."""
    conreq_config = ConreqConfig.get_solo()

    is_anime = content_discovery.is_anime(tmdb_id, "movie")
    all_root_dirs = content_manager.radarr_root_dirs()

    if is_anime:
        radarr_root = is_key_value_in_list(
            "id", conreq_config.radarr_anime_folder, all_root_dirs, return_item=True
        )["path"]
        radarr_profile_id = conreq_config.radarr_anime_quality_profile

    else:
        radarr_root = is_key_value_in_list(
            "id", conreq_config.radarr_movies_folder, all_root_dirs, return_item=True
        )["path"]
        radarr_profile_id = conreq_config.radarr_movies_quality_profile

    return {
        "radarr_profile_id": radarr_profile_id,
        "radarr_root": radarr_root,
    }


def initialize_conreq(conreq_config, form):
    """Sets up the initial database values during Conreq's first run sequence."""
    # Obtain the sonarr/radarr parameters
    conreq_config.sonarr_url = form.cleaned_data.get("sonarr_url")
    conreq_config.sonarr_api_key = form.cleaned_data.get("sonarr_api_key")
    conreq_config.radarr_url = form.cleaned_data.get("radarr_url")
    conreq_config.radarr_api_key = form.cleaned_data.get("radarr_api_key")

    # Generate the Conreq API key
    if not conreq_config.conreq_api_key:
        conreq_config.conreq_api_key = token_hex(16)

    # Enable Sonarr if URL and API key is configured
    if conreq_config.sonarr_url and conreq_config.sonarr_api_key:
        conreq_config.sonarr_enabled = True

    # Enable Radarr if URL and API key is configured
    if conreq_config.radarr_url and conreq_config.radarr_api_key:
        conreq_config.radarr_enabled = True

    # Remember that the database has been initialized
    conreq_config.conreq_initialized = True
    conreq_config.save()


def add_request_to_db(content_id, source, user):
    if not len(
        UserRequest.objects.filter(
            content_id=content_id, source=source, requested_by=user
        )
    ):
        new_request = UserRequest(
            content_id=content_id,
            source=source,
            requested_by=user,
        )
        new_request.clean_fields()
        new_request.save()

        log.handler(
            "Added " + str(content_id) + " to the user request database.",
            log.DEBUG,
            __logger,
        )
