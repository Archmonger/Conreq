from conreq.core.issue_reporting.models import ReportedIssue
from conreq.core.tmdb.discovery import TmdbDiscovery
from conreq.core.arrs.sonarr_radarr import ArrManager
from conreq.utils import log

_logger = log.get_logger(__name__)

# (Issue name, Resolution)
ISSUE_LIST = [
    ("Video does not match what was expected.", ["RENAME CONTENT", "REDOWNLOAD VIDEO"]),
    ("Video does not load.", ["REDOWNLOAD VIDEO"]),
    (
        "Video does not exist or is missing.",
        ["CHANGE ROOT FOLDER", "RENAME CONTENT", "REDOWNLOAD VIDEO"],
    ),
    ("Video is in the wrong category/folder.", ["CHANGE ROOT FOLDER"]),
    ("Wrong video length.", ["REDOWNLOAD VIDEO"]),
    ("Wrong audio language.", ["REDOWNLOAD VIDEO"]),
    ("Wrong subtitle language.", ["REDOWNLOAD SUBTITLES"]),
    ("Low quality video.", ["UPGRADE VIDEO"]),
    ("Bad or corrupt video.", ["REDOWNLOAD VIDEO"]),
    ("Bad or corrupt audio.", ["REDOWNLOAD VIDEO"]),
    ("Bad subtitles.", ["REDOWNLOAD SUBTITLES"]),
    ("Missing subtitles.", ["REDOWNLOAD SUBTITLES"]),
    ("Cannot request.", ["NOTIFY ADMIN"]),
    ("Other.", ["NOTIFY ADMIN"]),
]


def generate_issue_cards(reported_issues):
    """Retruns a list of cards"""
    content_discovery = TmdbDiscovery()
    content_manager = ArrManager()
    all_cards = []
    card = None
    for entry in reported_issues.values(
        "id",
        "reported_by__username",
        "content_id",
        "source",
        "resolved",
        "content_type",
        "issues",
        "seasons",
        "episodes",
    ):
        # Fetch TMDB entry
        if entry["source"] == "tmdb":
            card = content_discovery.get_by_tmdb_id(
                tmdb_id=entry["content_id"],
                content_type=entry["content_type"],
                obtain_extras=False,
            )
            if card is not None:
                all_cards.append({**card, **entry})

        # Fetch TVDB entry
        if entry["source"] == "tvdb":
            # Attempt to convert card to TMDB
            conversion = content_discovery.get_by_tvdb_id(tvdb_id=entry["content_id"])
            # Conversion found
            if conversion and conversion.get("tv_results"):
                card = conversion["tv_results"][0]
                all_cards.append({**card, **entry})

                # Convert all requests to use this new ID
                old_requests = ReportedIssue.objects.filter(
                    content_id=entry["content_id"], source="tvdb"
                )
                old_requests.update(content_id=card["id"], source="tmdb")
                log.handler(
                    entry["content_type"]
                    + " from "
                    + entry["source"]
                    + " with ID "
                    + entry["content_id"]
                    + " has been converted to TMDB",
                    log.INFO,
                    _logger,
                )

            # Fallback to checking sonarr's database
            else:
                card = content_manager.get(tvdb_id=entry["content_id"])
                all_cards.append({**card, **entry})

        if card is None:
            log.handler(
                entry["content_type"]
                + " from "
                + entry["source"]
                + " with ID "
                + entry["content_id"]
                + " no longer exists!",
                log.WARNING,
                _logger,
            )

    return all_cards
