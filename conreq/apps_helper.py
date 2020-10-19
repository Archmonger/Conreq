from conreq.core import log
from conreq import content_discovery, content_manager

__logger = log.get_logger("Content Discovery")
log.configure(__logger, log.DEBUG)

static_context_vars = {
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
    res = {**dict1, **static_context_vars}
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
                "TMDB card did not contan title or name!",
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
        # If a TMDB card was passed in, use it's respective function
        if card.__contains__("tmdbCard"):
            tmdb_conreq_status(card)

        # Compute conreq status of TV show
        elif card["contentType"] == "tv":
            content = content_manager.get(tvdb_id=card["tvdbId"])
            if content is not None:
                card["conreqStatus"] = content["conreqStatus"]

        # Compute conreq status of movie
        elif card["contentType"] == "movie":
            content = content_manager.get(tmdb_id=card["tmdbId"])
            if content is not None:
                card["conreqStatus"] = content["conreqStatus"]

        # Something unexpected was passed in
        else:
            log.handler(
                "TMDB card did not contan title or name!",
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