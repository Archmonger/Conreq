"""Conreq Searching: Searches for content."""

import tmdbsimple as tmdb

from conreq.core.server_settings.models import ConreqConfig
from conreq.core.tmdb.base import LANGUAGE, TmdbBase
from conreq.utils import cache, log

_logger = log.get_logger(__name__)

# Days, Hours, Minutes, Seconds
SEARCH_CACHE_TIMEOUT = 3 * 60 * 60


class TmdbSearch(TmdbBase):
    """Searches for a given query"""

    def __init__(self):
        # Database values
        self.conreq_config = ConreqConfig.get_solo()

    def all(self, query, page_number):
        """Search for a query. Sort the
        results based on their similiarity to the query.

        Args:
            query: A string containing a search term.
        """
        try:
            return self._remove_bad_content_types(
                self._set_content_attributes(
                    None,
                    cache.handler(
                        "search all",
                        page_key=page_number,
                        function=tmdb.Search().multi,
                        cache_duration=SEARCH_CACHE_TIMEOUT,
                        kwargs={
                            "page": page_number,
                            "query": query,
                            "language": LANGUAGE,
                        },
                    ),
                )
            )
        except Exception:
            log.handler(
                "Searching for all failed!",
                log.ERROR,
                _logger,
            )
            return []

    def television(self, query, page_number):
        """Search Sonarr for a query.

        Args:
            query: A string containing a search term.
            conreq_rank: Calculate conreq similarity ranking and sort the results (True/False)
        """
        try:
            return self._set_content_attributes(
                "tv",
                cache.handler(
                    "search tv",
                    page_key=page_number,
                    function=tmdb.Search().tv,
                    cache_duration=SEARCH_CACHE_TIMEOUT,
                    kwargs={
                        "page": page_number,
                        "query": query,
                        "language": LANGUAGE,
                    },
                ),
            )
        except Exception:
            log.handler(
                "Searching for TV failed!",
                log.ERROR,
                _logger,
            )
            return []

    def movie(self, query, page_number):
        """Search Radarr for a query.

        Args:
            query: A string containing a search term.
        """
        try:
            return self._set_content_attributes(
                "movie",
                cache.handler(
                    "search movie",
                    page_key=page_number,
                    function=tmdb.Search().movie,
                    cache_duration=SEARCH_CACHE_TIMEOUT,
                    kwargs={
                        "page": page_number,
                        "query": query,
                        "language": LANGUAGE,
                    },
                ),
            )
        except Exception:
            log.handler(
                "Searching for movies failed!",
                log.ERROR,
                _logger,
            )
            return []
