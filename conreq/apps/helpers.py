from conreq import content_discovery, content_manager
from conreq.core import cache, log

__logger = log.get_logger("Apps Helper")
log.configure(__logger, log.DEBUG)

TMDB_BACKDROP_URL = "https://image.tmdb.org/t/p/original"
TMDB_POSTER_300_URL = "https://image.tmdb.org/t/p/w300"

STATIC_CONTEXT_VARS = {
    "available": "Available",
    "partial": "Partial",
    "downloading": "Downloading",
    "discover": "Discover",
    "tv_shows": "TV Shows",
    "movies": "Movies",
    "my_requests": "My Requests",
    "report_issue": "Report Issue",
    "manage_users": "Manage Users",
    "send_mass_email": "Send Mass Email",
    "view_all_requests": "View All Requests",
    "view_all_issues": "View All Issues",
    "task_queue": "Task Queue",
    "settings": "Settings",
    "youtube": "YouTube",
}


def generate_context(dict1):
    res = {**dict1, **STATIC_CONTEXT_VARS}
    return res


def __get_external_ids(**kwargs):
    return content_discovery.get_external_ids(kwargs["id"], kwargs["content_type"])


def set_multi_conreq_status(results):
    # Fetch Sonarr and Radarr libraries
    radarr_library = cache.handler(
        "radarr library cache",
    )
    sonarr_library = cache.handler(
        "sonarr library cache",
    )

    external_id_multi_fetch = {}

    # TODO: Protection against sonarr or radarr library being none due to expired cache
    for card in results:
        # Sonarr card
        if card.__contains__("tvdbId"):
            if sonarr_library is not None and sonarr_library.__contains__(
                card["tvdbId"]
            ):
                card["conreqStatus"] = sonarr_library[card["tvdbId"]]["conreqStatus"]

        # Radarr card
        elif card.__contains__("tmdbId"):
            if radarr_library is not None and radarr_library.__contains__(
                card["tmdbId"]
            ):
                card["conreqStatus"] = radarr_library[card["tmdbId"]]["conreqStatus"]

        # TMDB TV card
        elif card.__contains__("name"):
            # Format to multi-fetch external IDs from the database
            external_id_multi_fetch[str(card["id"])] = {
                "function": __get_external_ids,
                "cache_key": "tvexternalidcache_kwargs_key" + str(card["id"]),
                "kwargs": {"id": card["id"], "content_type": "tv"},
                "card": card,
            }

        # TMDB movie card
        elif card.__contains__("title"):
            if radarr_library is not None and radarr_library.__contains__(card["id"]):
                card["conreqStatus"] = radarr_library[card["id"]]["conreqStatus"]

    # Fetch all external IDs at once
    external_id_cache_results = cache.handler(
        "tv external id cache", external_id_multi_fetch
    )

    # Retrieve the external IDs at set the conreq status
    for cache_key, external_id_results in external_id_cache_results.items():
        key = cache_key.split("_")[2][3:]
        if sonarr_library is not None and sonarr_library.__contains__(
            external_id_results["tvdb_id"]
        ):
            external_id_multi_fetch[key]["card"]["conreqStatus"] = sonarr_library[
                external_id_results["tvdb_id"]
            ]["conreqStatus"]

    return results


def set_single_conreq_status(card):
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
