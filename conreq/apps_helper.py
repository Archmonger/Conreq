from conreq.core import log
from conreq import content_discovery, content_manager

__logger = log.get_logger("Content Discovery")
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


def tmdb_conreq_status(card):
    try:
        # Compute conreq status of TV show
        if card.__contains__("name"):
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
                "TMDB card did not contain title or name!",
                log.WARNING,
                __logger,
            )
            return card

    except:
        log.handler(
            "Could not determine Conreq Status of TMDB card!",
            log.ERROR,
            __logger,
        )
        return card


def arr_conreq_status(card):
    try:
        # Compute conreq status of a Sonarr/Radarr card
        if card.__contains__("contentType"):
            content = content_manager.get(tvdb_id=card["tvdbId"])
            if content is not None:
                card["conreqStatus"] = content["conreqStatus"]

        # Something unexpected was passed in
        else:
            log.handler(
                "TMDB card did not contain contentType!",
                log.WARNING,
                __logger,
            )
            return card

    except:
        log.handler(
            "Could not determine Conreq Status of TMDB card!",
            log.ERROR,
            __logger,
        )
        return card