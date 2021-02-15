"""Functions commonly used to construct views."""
from threading import Thread

from conreq.apps.server_settings.models import ConreqConfig
from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.utils import cache, log
from conreq.utils.generic import is_key_value_in_list

_logger = log.get_logger(__name__)


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


def generate_context(dict1):
    """Creates a context dictionary with common context variables."""
    res = {**dict1, **STATIC_CONTEXT_VARS}
    return res


def __set_many_availability(card, radarr_library, sonarr_library):
    """Threaded portion of set_many_availability."""
    # Sonarr card
    if card.__contains__("tvdbId"):
        if sonarr_library is not None and sonarr_library.__contains__(
            str(card["tvdbId"])
        ):
            card["availability"] = sonarr_library[str(card["tvdbId"])]["availability"]

    # Radarr card
    elif card.__contains__("tmdbId"):
        if radarr_library is not None and radarr_library.__contains__(
            str(card["tmdbId"])
        ):
            card["availability"] = radarr_library[str(card["tmdbId"])]["availability"]

    # TMDB TV card
    elif card.__contains__("name"):
        if (
            sonarr_library is not None
            and card.__contains__("tvdb_id")
            and sonarr_library.__contains__(str(card["tvdb_id"]))
        ):
            card["availability"] = sonarr_library[str(card["tvdb_id"])]["availability"]

    # TMDB movie card
    elif card.__contains__("title"):
        if radarr_library is not None and radarr_library.__contains__(str(card["id"])):
            card["availability"] = radarr_library[str(card["id"])]["availability"]


def set_many_availability(results):
    """Sets the availabily on list of cards."""
    # Fetch Sonarr and Radarr libraries
    radarr_library = cache.handler(
        "radarr library",
    )
    sonarr_library = cache.handler(
        "sonarr library",
    )

    # Generate the availability if possible, or get the external ID if a TVDB ID is needed
    thread_list = []
    for card in results:
        thread = Thread(
            target=__set_many_availability,
            args=[card, radarr_library, sonarr_library],
        )
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()

    return results


def set_single_availability(card):
    """Sets the availabily on a single card."""
    content_manager = ContentManager()
    content_discovery = ContentDiscovery()
    try:
        # Compute the availability of a Sonarr card
        if card.__contains__("tvdbId"):
            content = content_manager.get(tvdb_id=card["tvdbId"])
            if content is not None:
                card["availability"] = content["availability"]

        # Compute the availability of a Radarr card
        elif card.__contains__("tmdbId"):
            content = content_manager.get(tmdb_id=card["tmdbId"])
            if content is not None:
                card["availability"] = content["availability"]

        # Compute the availability of TV show
        elif card.__contains__("name"):
            external_id = content_discovery.get_external_ids(card["id"], "tv")
            content = content_manager.get(tvdb_id=external_id["tvdb_id"])
            if content is not None:
                card["availability"] = content["availability"]

        # Compute the availability of movie
        elif card.__contains__("title"):
            content = content_manager.get(tmdb_id=card["id"])
            if content is not None:
                card["availability"] = content["availability"]

        # Something unexpected was passed in
        else:
            log.handler(
                "Card did not contain contentType, title, or name!",
                log.WARNING,
                _logger,
            )
            return card

    except:
        log.handler(
            "Could not determine the availability of card!\n" + str(card),
            log.ERROR,
            _logger,
        )
        return card


def obtain_sonarr_parameters(
    content_discovery,
    content_manager,
    tmdb_id=None,
    tvdb_id=None,
):
    """Returns the common parameters needed for adding a series to Sonarr."""
    conreq_config = ConreqConfig.get_solo()

    # Attempt to convert TVDB to TMDB if possible
    if tmdb_id is None:
        conversion = content_discovery.get_by_tvdb_id(tvdb_id)
        if conversion.__contains__("tv_results") and conversion["tv_results"]:
            tmdb_id = conversion["tv_results"][0]["id"]

    # Determine series type, root directory, and profile ID
    is_anime = False
    if tmdb_id is not None:
        is_anime = content_discovery.is_anime(tmdb_id, "tv")

    season_folders = conreq_config.sonarr_season_folders
    all_root_dirs = content_manager.sonarr_root_dirs()

    # Generate parameters
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


def add_unique_to_db(model, **kwargs):
    """Adds a row to the database only if all parameters are unique."""
    if not model.objects.filter(**kwargs):
        new_request = model(**kwargs)
        new_request.clean_fields()
        new_request.save()
