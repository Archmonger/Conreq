"""Globals and Helpers for TMDB content discovery."""
from random import shuffle

import tmdbsimple as tmdb
from django.conf import settings

from conreq.utils import cache, log
from conreq.utils.generic import is_key_value_in_list
from conreq.utils.threads import ReturnThread

# TMDB API key is safe to hard-code. It can only access publicly available data.
tmdb.API_KEY = "112fd4c96274603f68620c78067d5422"
_logger = log.get_logger(__name__)
_timezone = getattr(settings, "TIME_ZONE")

# Globals
ANIME_CHECK_FALLBACK = True
LANGUAGE = "en-US"
MAX_RECOMMENDED_PAGES = 10
MAX_SHUFFLED_PAGES = 30
# Days, Hours, Minutes, Seconds
EXTERNAL_ID_CACHE_TIMEOUT = 7 * 24 * 60 * 60
DISCOVER_CACHE_TIMEOUT = 3 * 24 * 60 * 60
GET_BY_TMDB_ID_CACHE_TIMEOUT = 4 * 60 * 60
GET_BY_TVDB_ID_CACHE_TIMEOUT = 4 * 60 * 60
GET_GENRES_CACHE_TIMEOUT = 30 * 24 * 60 * 60
IS_ANIME_CACHE_TIMEOUT = 7 * 24 * 60 * 60
RECOMMENDED_CACHE_TIMEOUT = 14 * 24 * 60 * 60
SIMILAR_CACHE_TIMEOUT = 14 * 24 * 60 * 60
COLLECTION_CACHE_TIMEOUT = 14 * 24 * 60 * 60
PERSON_CACHE_TIMEOUT = 14 * 24 * 60 * 60
SHUFFLED_PAGE_CACHE_TIMEOUT = 1 * 24 * 60 * 60


class TmdbBase:
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
            # Determine if a specific ID is anime (True/False)
            if content_type == "tv":
                return cache.handler(
                    "is tv anime",
                    function=self._is_tv_anime,
                    cache_duration=IS_ANIME_CACHE_TIMEOUT,
                    args=[tmdb_id],
                )

            # Determine if a specific ID is anime (True/False)
            if content_type == "movie":
                return cache.handler(
                    "is movie anime",
                    function=self._is_movie_anime,
                    cache_duration=IS_ANIME_CACHE_TIMEOUT,
                    args=[tmdb_id],
                )

            # Content Type was invalid
            log.handler(
                f"Invalid content_type {str(content_type)} in is_anime().",
                log.WARNING,
                _logger,
            )

        except Exception:
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
                f"Invalid content_type {str(content_type)} in get_external_ids().",
                log.WARNING,
                _logger,
            )

        except Exception:
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
                f"Invalid content_type {str(content_type)} in get_genres().",
                log.WARNING,
                _logger,
            )

        except Exception:
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
        for result in tmdb_response:
            # TMDB TV card
            if isinstance(result, dict) and result.__contains__("name"):
                # Valid ID defaults to false until a TVDB match is determined
                result["conreq_valid_id"] = False
                external_id_multi_fetch[str(result["id"])] = {
                    "function": tmdb.TV(result["id"]).external_ids,
                    "kwargs": {},
                    "args": [],
                    "card": result,  # Store the card in here to make it slightly easier to find later
                }

            # TMDB Movie card
            elif isinstance(result, dict) and result.__contains__("title"):
                result["conreq_valid_id"] = True

        # Grab external IDs if needed
        if external_id_multi_fetch:
            external_id_multi_fetch_results = cache.multi_handler(
                "get tv external ids",
                functions=external_id_multi_fetch,
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

                except Exception:
                    pass

        return tmdb_response

    def _multi_page_fetch(
        self, cache_name, function, page_number, page_multiplier, **kwargs
    ):
        """Obtains multiple pages of results at once via threads."""
        total_pages = page_number * page_multiplier
        thread_list = []
        for subtractor in reversed(range(page_multiplier)):
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
        self.determine_id_validity(merged_results["results"])

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

                else:
                    # Set the total pages to the smallest value
                    merged_results["total_pages"] = min(
                        merged_results["total_pages"], result["total_pages"]
                    )
                    # Set the total results to the smallest value
                    merged_results["total_results"] = min(
                        merged_results["total_results"], result["total_results"]
                    )
                    # Merge the search results
                    merged_results["results"] = (
                        merged_results["results"] + result["results"]
                    )

            return self._remove_duplicate_results(merged_results)

        except Exception:
            log.handler(
                "Failed to merge results!",
                log.ERROR,
                _logger,
            )
        return None

    @staticmethod
    def _shuffle_results(query):
        """Shuffle API results"""
        try:
            shuffle(query["results"])
            return query

        except Exception:
            log.handler(
                "Failed to shuffle results!",
                log.ERROR,
                _logger,
            )
        return None

    @staticmethod
    def _remove_duplicate_results(query):
        """Removes duplicates from a dict"""
        try:
            results = query["results"].copy()

            # Keys used to determine if duplicates exist
            unique_tv_keys = {}
            unique_movie_keys = {}

            clean_results = []
            for entry in results:
                # Remove duplicate TV
                if entry.__contains__("name"):
                    if not unique_tv_keys.__contains__(entry["name"]):
                        clean_results.append(entry)
                    unique_tv_keys[entry["name"]] = True

                elif entry.__contains__("title"):
                    if not unique_movie_keys.__contains__(entry["title"]):
                        clean_results.append(entry)
                    unique_movie_keys[entry["title"]] = True

                else:
                    log.handler(
                        f"While removing duplicates, entry found that did not contain name or title!{str(entry)}",
                        log.WARNING,
                        _logger,
                    )

            query["results"] = clean_results
            return query

        except Exception:
            log.handler(
                "Failed to remove duplicate results!",
                log.ERROR,
                _logger,
            )
        return None

    @staticmethod
    def _shuffled_page_numbers():
        """Cacheable part of shuffled_page_numbers()"""
        temp_list = [*range(1, MAX_SHUFFLED_PAGES + 1)]
        shuffle(temp_list)
        return dict(enumerate(temp_list, start=1))

    @staticmethod
    def _is_tv_anime(tmdb_id):
        """Cacheable part of is_tv_anime()"""
        api_results = tmdb.TV(tmdb_id).keywords()

        # Check if the content contains Keyword: Anime
        if is_key_value_in_list("name", "anime", api_results["results"]):
            log.handler(f"{str(tmdb_id)} is anime.", log.INFO, _logger)
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
                    f"{str(tmdb_id)} is anime, based on fallback detection.",
                    log.INFO,
                    _logger,
                )
                return True

        log.handler(f"{str(tmdb_id)} is not anime.", log.INFO, _logger)
        return False

    @staticmethod
    def _is_movie_anime(tmdb_id):
        """Cacheable part of is_movie_anime()"""
        api_results = tmdb.Movies(tmdb_id).keywords()

        # Check if the content contains Keyword: Anime
        if is_key_value_in_list("name", "anime", api_results["keywords"]):
            log.handler(f"{str(tmdb_id)} is anime.", log.INFO, _logger)
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
                    f"{str(tmdb_id)} is anime, based on fallback detection.",
                    log.INFO,
                    _logger,
                )
                return True

        log.handler(f"{str(tmdb_id)} is not anime.", log.INFO, _logger)
        return False

    @staticmethod
    def _set_content_attributes(content_type, results):
        """Sets the content type as tv/movie and content source as "tmdb" on a list of results"""
        try:
            # Set a list of results
            if isinstance(results, dict) and results.__contains__("results"):
                for result in results["results"]:
                    # Use the media type in TMDB Search endpoint if available
                    result["content_type"] = (
                        content_type if content_type else result.get("media_type")
                    )
            # Special case for "Collections"
            elif isinstance(results, dict) and results.__contains__("parts"):
                for result in results["parts"]:
                    result["content_type"] = content_type
            # Special case for "Person" with tv/movies appended
            elif isinstance(results, dict) and (
                results.__contains__("tv_credits")
                or results.__contains__("movie_credits")
            ):
                for result in results["tv_credits"]["cast"]:
                    result["content_type"] = "tv"
                for result in results["tv_credits"]["crew"]:
                    result["content_type"] = "tv"
                for result in results["movie_credits"]["cast"]:
                    result["content_type"] = "movie"
                for result in results["movie_credits"]["crew"]:
                    result["content_type"] = "movie"
            # Special case for get_content_by_tvdb_id
            elif isinstance(results, list):
                for result in results:
                    result["content_type"] = content_type
            # # Set a single media item
            elif isinstance(results, dict):
                results["content_type"] = content_type
        except Exception:
            log.handler(
                "Failed to set content attributes!",
                log.ERROR,
                _logger,
            )

        return results

    @staticmethod
    def _remove_bad_content_types(results):
        """Removes results that aren't TV or movies"""
        new_results = None
        try:
            # Set a list of results
            if isinstance(results, dict) and results.__contains__("results"):
                new_results = results.copy()
                new_results["results"] = []
                for result in results["results"]:
                    content_type = result.get("content_type")
                    if content_type in ("movie", "tv"):
                        new_results["results"].append(result)
                return new_results
        except Exception:
            log.handler(
                "Failed to set content attributes!",
                log.ERROR,
                _logger,
            )

        return results
