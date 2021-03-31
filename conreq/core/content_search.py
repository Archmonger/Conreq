"""Conreq Searching: Searches for content."""

import tmdbsimple as tmdb
from conreq.apps.server_settings.models import ConreqConfig
from conreq.core.content_discovery.tmdb_base import Base, LANGUAGE
from conreq.utils import cache, log

_logger = log.get_logger(__name__)

# Days, Hours, Minutes, Seconds
SEARCH_CACHE_TIMEOUT = 60 * 60


class Search(Base):
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
            results = self._remove_bad_content_types(
                self._set_content_attributes(
                    None,
                    tmdb.Search().multi(
                        page=page_number, query=query, language=LANGUAGE
                    ),
                )
            )
            return results

        except:
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
            results = self._set_content_attributes(
                "tv",
                tmdb.Search().tv(page=page_number, query=query, language=LANGUAGE),
            )
            return results

        except:
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
            results = self._set_content_attributes(
                "movie",
                tmdb.Search().movie(page=page_number, query=query, language=LANGUAGE),
            )
            return results

        except:
            log.handler(
                "Searching for movies failed!",
                log.ERROR,
                _logger,
            )
            return []
