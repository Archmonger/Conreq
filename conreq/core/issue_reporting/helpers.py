from conreq.core.tmdb.discovery import TmdbDiscovery
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
    all_cards = []
    card = None
    for entry in reported_issues:
        # Fetch TMDB entry
        card = content_discovery.get_by_tmdb_id(
            tmdb_id=entry["content_id"],
            content_type=entry["content_type"],
            obtain_extras=False,
        )
        if card is not None:
            all_cards.append({**card, **entry})

        if card is None:
            log.handler(
                entry["content_type"]
                + " with ID "
                + entry["content_id"]
                + " no longer exists!",
                log.WARNING,
                _logger,
            )

    return all_cards
