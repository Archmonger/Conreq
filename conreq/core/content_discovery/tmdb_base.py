"""Globals and Helpers for TMDB content discovery."""
from random import shuffle

import tmdbsimple as tmdb
from conreq.utils import cache, log
from conreq.utils.generic import is_key_value_in_list
from conreq.utils.multiprocessing import ReturnThread
from tzlocal import get_localzone

# TMDB API key is safe to hard-code. It can only access publicly available data.
tmdb.API_KEY = "112fd4c96274603f68620c78067d5422"
_logger = log.get_logger(__name__)
_timezone = get_localzone().zone

# Globals
ANIME_CHECK_FALLBACK = True
LANGUAGE = "en-US"
MAX_RECOMMENDED_PAGES = 7
MAX_SHUFFLED_PAGES = 30
# Days, Hours, Minutes, Seconds
EXTERNAL_ID_CACHE_TIMEOUT = 7 * 24 * 60 * 60
DISCOVER_CACHE_TIMEOUT = 3 * 24 * 60 * 60
GET_BY_TMDB_ID_CACHE_TIMEOUT = 7 * 24 * 60 * 60
GET_BY_TVDB_ID_CACHE_TIMEOUT = 7 * 24 * 60 * 60
GET_GENRES_CACHE_TIMEOUT = 30 * 24 * 60 * 60
IS_ANIME_CACHE_TIMEOUT = 7 * 24 * 60 * 60
RECOMMENDED_CACHE_TIMEOUT = 14 * 24 * 60 * 60
SIMILAR_CACHE_TIMEOUT = 14 * 24 * 60 * 60
COLLECTION_CACHE_TIMEOUT = 14 * 24 * 60 * 60
KEYWORDS_TO_IDS_CACHE_TIMEOUT = 30 * 24 * 60 * 60
SHUFFLED_PAGE_CACHE_TIMEOUT = 1 * 24 * 60 * 60


class Base:
    """Helper methods for TMDB content discovery."""

    def is_anime(self, tmdb_id, content_type):
        """Checks if a TMDB ID can be considered Anime.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".

        Returns:
            True/False
        """
        try:
            # TV: Obtain the keywords for a specific ID
            if content_type == "tv":
                return cache.handler(
                    "is tv anime",
                    function=self._is_tv_anime,
                    cache_duration=IS_ANIME_CACHE_TIMEOUT,
                    args=[tmdb_id],
                )

            # Movies: Obtain the keywords for a specific ID
            if content_type == "movie":
                return cache.handler(
                    "is movie anime",
                    function=self._is_movie_anime,
                    cache_duration=IS_ANIME_CACHE_TIMEOUT,
                    args=[tmdb_id],
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in is_anime().",
                log.WARNING,
                _logger,
            )

        except:
            log.handler(
                "Failed to check if content is anime!",
                log.ERROR,
                _logger,
            )
            return False
        return None

    @staticmethod
    def get_external_ids(tmdb_id, content_type):
        """Gets all external IDs given a TMDB ID.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
        """
        try:
            # Obtain a movie's external IDs
            if content_type == "movie":
                return cache.handler(
                    "get movie external ids",
                    page_key=tmdb_id,
                    function=tmdb.Movies(tmdb_id).external_ids,
                    cache_duration=EXTERNAL_ID_CACHE_TIMEOUT,
                )

            # Obtain a TV show's external IDs
            if content_type == "tv":
                return cache.handler(
                    "get tv external ids",
                    function=tmdb.TV(tmdb_id).external_ids,
                    page_key=tmdb_id,
                    cache_duration=EXTERNAL_ID_CACHE_TIMEOUT,
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in get_external_ids().",
                log.WARNING,
                _logger,
            )

        except:
            log.handler(
                "Failed to obtain external ID!",
                log.ERROR,
                _logger,
            )
        return None

    @staticmethod
    def get_genres(content_type):
        """Gets all available TMDB genres and genre IDs.

        Args:
            content_type: String containing "movie" or "tv".
        """
        try:
            # Obtain a movie's genres
            if content_type == "movie":
                return cache.handler(
                    "get all movie genres",
                    function=tmdb.Genres().movie_list,
                    cache_duration=GET_GENRES_CACHE_TIMEOUT,
                )

            # Obtain a TV show's genres
            if content_type == "tv":
                return cache.handler(
                    "get all tv genres",
                    function=tmdb.Genres().tv_list,
                    cache_duration=GET_GENRES_CACHE_TIMEOUT,
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in get_genres().",
                log.WARNING,
                _logger,
            )

        except:
            log.handler(
                "Failed to obtain genres!",
                log.ERROR,
                _logger,
            )
        return None

    @staticmethod
    def determine_id_validity(tmdb_response):
        """Determine if a movie has a TMDB ID, and if TV has a TVDB ID.
        Required because TVDB IDs are required for Sonarr"""
        external_id_multi_fetch = {}
        external_id_multi_fetch_results = None

        # Create a list of all needed IDs
        for result in tmdb_response["results"]:
            # Sonarr card
            if result.__contains__("tvdbId"):
                result["conreq_valid_id"] = True

            # Radarr card
            elif result.__contains__("tmdbId"):
                result["conreq_valid_id"] = True

            # TMDB TV card
            elif result.__contains__("name"):
                # Valid ID defaults to false until a TVDB match is determined
                result["conreq_valid_id"] = False
                external_id_multi_fetch[str(result["id"])] = {
                    "function": tmdb.TV(result["id"]).external_ids,
                    "kwargs": {},
                    "args": [],
                    "card": result,  # Store the card in here to make it slightly easier to find later
                }

            # TMDB Movie card
            elif result.__contains__("title"):
                result["conreq_valid_id"] = True

        # Grab external IDs if needed
        if external_id_multi_fetch:
            external_id_multi_fetch_results = cache.handler(
                "get tv external ids",
                function=external_id_multi_fetch,
                cache_duration=EXTERNAL_ID_CACHE_TIMEOUT,
            )

        # Check if a TMDB TV show has a TVDB ID
        if external_id_multi_fetch_results:
            for (
                cache_key,
                external_id_results,
            ) in external_id_multi_fetch_results.items():
                key = cache.obtain_key_from_cache_key(cache_key)
                try:
                    # Does an ID exist?
                    if external_id_results["tvdb_id"]:
                        # Set the ID validity
                        external_id_multi_fetch[key]["card"]["conreq_valid_id"] = True
                        external_id_multi_fetch[key]["card"][
                            "tvdb_id"
                        ] = external_id_results["tvdb_id"]

                except:
                    pass

    def _multi_page_fetch(
        self, cache_name, function, page_number, page_multiplier, **kwargs
    ):
        """Obtains multiple pages of results at once via threads."""
        total_pages = page_number * page_multiplier
        thread_list = []
        for subtractor in reversed(range(0, page_multiplier)):
            thread_kwargs = {
                **{"page": total_pages - subtractor, "language": LANGUAGE},
                **kwargs,
            }
            thread = ReturnThread(
                target=cache.handler,
                args=[
                    cache_name,
                ],
                kwargs={
                    "function": function,
                    "page_key": total_pages - subtractor,
                    "cache_duration": DISCOVER_CACHE_TIMEOUT,
                    "kwargs": thread_kwargs,
                },
            )
            thread.start()
            thread_list.append(thread)

        # Merge together these pages
        merged_results = thread_list[0].join()
        thread_list.remove(thread_list[0])
        for thread in thread_list:
            merged_results = self._merge_results(merged_results, thread.join())

        # Determine if TV has a TVDB ID (required for Sonarr)
        self.determine_id_validity(merged_results)

        return merged_results

    def _merge_results(self, *args):
        """Merge multiple API results into one"""
        try:
            first_run = True
            merged_results = {}

            for result in args:
                # On the first run, set up the initial dictionary
                if first_run:
                    merged_results = result.copy()
                    first_run = False

                # On subsequent runs, update or merge the values if needed
                else:
                    # Set the total pages to the smallest value
                    if merged_results["total_pages"] > result["total_pages"]:
                        merged_results["total_pages"] = result["total_pages"]

                    # Set the total results to the smallest value
                    if merged_results["total_results"] > result["total_results"]:
                        merged_results["total_results"] = result["total_results"]

                    # Merge the search results
                    merged_results["results"] = (
                        merged_results["results"] + result["results"]
                    )

            return self._remove_duplicate_results(merged_results)

        except:
            log.handler(
                "Failed to merge results!",
                log.ERROR,
                _logger,
            )
        return {}

    @staticmethod
    def _shuffle_results(query):
        """Shuffle API results"""
        try:
            shuffle(query["results"])
            return query

        except:
            log.handler(
                "Failed to shuffle results!",
                log.ERROR,
                _logger,
            )
            return {}

    @staticmethod
    def _remove_duplicate_results(query):
        """Removes duplicates from a dict"""
        try:
            results = query["results"].copy()

            # Results with no duplicates
            clean_results = []

            # Keys used to determine if duplicates exist
            unique_tv_keys = {}
            unique_movie_keys = {}

            for entry in results:
                # Remove duplicate TV
                if entry.__contains__("name"):
                    if not unique_tv_keys.__contains__(entry["name"]):
                        clean_results.append(entry)
                    unique_tv_keys[entry["name"]] = True

                # Remove duplicate movies
                elif entry.__contains__("title"):
                    if not unique_movie_keys.__contains__(entry["title"]):
                        clean_results.append(entry)
                    unique_movie_keys[entry["title"]] = True

                # Something unexpected happened
                else:
                    log.handler(
                        "While removing duplicates, entry found that did not contain name or title!"
                        + str(entry),
                        log.WARNING,
                        _logger,
                    )

            query["results"] = clean_results
            return query

        except:
            log.handler(
                "Failed to remove duplicate results!",
                log.ERROR,
                _logger,
            )

    @staticmethod
    def _shuffled_page_numbers():
        """Cacheable part of shuffled_page_numbers()"""
        temp_list = [*range(1, MAX_SHUFFLED_PAGES + 1)]
        shuffle(temp_list)
        return dict(enumerate(temp_list, start=1))

    @staticmethod
    def _keywords_to_ids(keywords):
        """Turn a keyword string or a list of keywords into a TMDB keyword ID number"""
        try:
            keyword_ids = []

            # A list of keywords was given
            if len(keywords) >= 1 and isinstance(keywords, list):
                for keyword in keywords:
                    # Perform a search
                    keyword_search = cache.handler(
                        "keyword to id",
                        page_key=keyword,
                        function=tmdb.Search().keyword,
                        cache_duration=KEYWORDS_TO_IDS_CACHE_TIMEOUT,
                        kwargs={
                            "query": keyword,
                        },
                    )["results"]

                    for search_result in keyword_search:
                        # Find an exact match
                        if search_result["name"].lower() == keyword.lower():
                            # Return the keyword ID number
                            keyword_ids.append(search_result["id"])

            # A single keyword was given
            elif len(keywords) >= 1 and isinstance(keywords, str):
                # Perform a search
                keyword_search = cache.handler(
                    "keyword to id",
                    page_key=keywords,
                    function=tmdb.Search().keyword,
                    cache_duration=KEYWORDS_TO_IDS_CACHE_TIMEOUT,
                    kwargs={
                        "query": keyword,
                    },
                )["results"]

                for search_result in keyword_search:
                    # Find an exact match
                    if search_result["name"].lower() == keywords.lower():
                        # Return the keyword ID number
                        keyword_ids.append(search_result["id"])

            # User put in args in an improper format
            else:
                log.handler(
                    "Keyword(s) "
                    + str(keywords)
                    + " were provided in an improper format",
                    log.WARNING,
                    _logger,
                )
                return None

            # We managed to obtain at least one ID
            if len(keyword_ids) >= 1:
                return keyword_ids

            # We couldn't obtain any IDs
            log.handler(
                "Keyword(s) " + str(keywords) + " not found!",
                log.INFO,
                _logger,
            )

        except:
            log.handler(
                "Failed to obtain keyword!",
                log.ERROR,
                _logger,
            )
        return None

    @staticmethod
    def _is_tv_anime(tmdb_id):
        """Cacheable part of is_tv_anime()"""
        api_results = tmdb.TV(tmdb_id).keywords()

        # Check if the content contains Keyword: Anime
        if is_key_value_in_list("name", "anime", api_results["results"]):
            log.handler(
                str(tmdb_id) + " is anime.",
                log.INFO,
                _logger,
            )
            return True

        # Check if fallback method is enabled
        if ANIME_CHECK_FALLBACK:
            tv_info = tmdb.TV(tmdb_id).info()
            # Check if genere is Animation and Country is Japan
            if (
                is_key_value_in_list("name", "Animation", tv_info["genres"])
                and "JP" in tv_info["origin_country"]
            ):
                log.handler(
                    str(tmdb_id) + " is anime, based on fallback detection.",
                    log.INFO,
                    _logger,
                )
                return True

        log.handler(
            str(tmdb_id) + " is not anime.",
            log.INFO,
            _logger,
        )
        return False

    @staticmethod
    def _is_movie_anime(tmdb_id):
        """Cacheable part of is_movie_anime()"""
        api_results = tmdb.Movies(tmdb_id).keywords()

        # Check if the content contains Keyword: Anime
        if is_key_value_in_list("name", "anime", api_results["keywords"]):
            log.handler(
                str(tmdb_id) + " is anime.",
                log.INFO,
                _logger,
            )
            return True

        # Check if fallback method is enabled
        if ANIME_CHECK_FALLBACK:
            movie_info = tmdb.Movies(tmdb_id).info()

            # Check if genere is Animation and Country is Japan
            if is_key_value_in_list(
                "name", "Animation", movie_info["genres"]
            ) and is_key_value_in_list(
                "iso_3166_1", "JP", movie_info["production_countries"]
            ):
                log.handler(
                    str(tmdb_id) + " is anime, based on fallback detection.",
                    log.INFO,
                    _logger,
                )
                return True

        log.handler(
            str(tmdb_id) + " is not anime.",
            log.INFO,
            _logger,
        )
        return False

    @staticmethod
    def _set_content_attributes(content_type, results):
        """Sets the content type as tv/movie and content source as "tmdb" on a list of results"""
        try:
            # Set a list of results
            if isinstance(results, dict) and results.__contains__("results"):
                for result in results["results"]:
                    result["content_type"] = content_type
                    result["content_source"] = "tmdb"
            # Special case for "Collections"
            elif isinstance(results, dict) and results.__contains__("parts"):
                for result in results["parts"]:
                    result["content_type"] = content_type
                    result["content_source"] = "tmdb"
            # Special case for get_content_by_tvdb_id
            elif isinstance(results, list):
                for result in results:
                    result["content_type"] = content_type
                    result["content_source"] = "tmdb"
            # # Set a single media item
            else:
                results["content_type"] = content_type
                results["content_source"] = "tmdb"
        except:
            log.handler(
                "Failed to set content attributes!",
                log.ERROR,
                _logger,
            )

        return results
