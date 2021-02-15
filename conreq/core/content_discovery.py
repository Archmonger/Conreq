"""Conreq Content Discovery: Searches TMDB for content."""
from random import shuffle

import tmdbsimple as tmdb
from conreq.utils import cache, log
from conreq.utils.generic import is_key_value_in_list
from conreq.utils.multiprocessing import ReturnThread, threaded_execution

_logger = log.get_logger(__name__)

# Globals
ANIME_CHECK_FALLBACK = True
LANGUAGE = "en"
MAX_RECOMMENDED_PAGES = 7
MAX_SIMILAR_PAGES = 1
MAX_SHUFFLED_PAGES = 30
# Days, Hours, Minutes, Seconds
EXTERNAL_ID_CACHE_TIMEOUT = 7 * 24 * 60 * 60
DISCOVER_BY_FILTER_CACHE_TIMEOUT = 3 * 24 * 60 * 60
GET_BY_TMDB_ID_CACHE_TIMEOUT = 7 * 24 * 60 * 60
GET_BY_TVDB_ID_CACHE_TIMEOUT = 7 * 24 * 60 * 60
GET_GENRES_CACHE_TIMEOUT = 30 * 24 * 60 * 60
IS_ANIME_CACHE_TIMEOUT = 7 * 24 * 60 * 60
RECOMMENDED_CACHE_TIMEOUT = 14 * 24 * 60 * 60
SIMILAR_CACHE_TIMEOUT = 14 * 24 * 60 * 60
COLLECTION_CACHE_TIMEOUT = 14 * 24 * 60 * 60
POPULAR_AND_TOP_CACHE_TIMEOUT = 3 * 24 * 60 * 60
KEYWORDS_TO_IDS_CACHE_TIMEOUT = 30 * 24 * 60 * 60
SHUFFLED_PAGE_CACHE_TIMEOUT = 1 * 24 * 60 * 60


class ContentDiscovery:
    """Discovers top, trending, and recommended content using TMDB as the backend.

    Args:
        tmdb_api_key: String containing the TMDB API key.
    """

    def __init__(self):
        # TMDB API key is safe to hard-code. It can only access publicly available data.
        tmdb.API_KEY = "112fd4c96274603f68620c78067d5422"

    # Public class methods
    def all(self, page_number, page_multiplier=1):
        """Get top and popular content from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        # Shuffle the order of the first N many pages for randomized discovery
        if page_number <= MAX_SHUFFLED_PAGES:
            page = cache.handler(
                "discover all page numbers",
                function=self.__shuffled_page_numbers,
                cache_duration=SHUFFLED_PAGE_CACHE_TIMEOUT,
            )[page_number]
        else:
            page = page_number

        return cache.handler(
            "discover all",
            page_key=page,
            function=self.__all,
            cache_duration=SHUFFLED_PAGE_CACHE_TIMEOUT,
            args=[page, page_multiplier],
        )

    def tv(self, page_number, page_multiplier=1):
        """Get top and popular TV from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        # Shuffle the order of the first N many pages for randomized discovery
        if page_number <= MAX_SHUFFLED_PAGES:
            page = cache.handler(
                "discover tv page numbers",
                function=self.__shuffled_page_numbers,
                cache_duration=SHUFFLED_PAGE_CACHE_TIMEOUT,
            )[page_number]
        else:
            page = page_number

        return cache.handler(
            "discover tv",
            page_key=page,
            function=self.__tv,
            cache_duration=SHUFFLED_PAGE_CACHE_TIMEOUT,
            args=[page, page_multiplier],
        )

    def movies(self, page_number, page_multiplier=1):
        """Get top and popular TV from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        # Shuffle the order of the first N many pages for randomized discovery
        if page_number <= MAX_SHUFFLED_PAGES:
            page = cache.handler(
                "discover movies page numbers",
                function=self.__shuffled_page_numbers,
                cache_duration=SHUFFLED_PAGE_CACHE_TIMEOUT,
            )[page_number]
        else:
            page = page_number

        return cache.handler(
            "discover movies",
            page_key=page,
            function=self.__movies,
            cache_duration=SHUFFLED_PAGE_CACHE_TIMEOUT,
            args=[page, page_multiplier],
        )

    def popular(self, page_number, page_multiplier=1):
        """Get popular content from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__popular(page_number, page_multiplier)

    def top(self, page_number, page_multiplier=1):
        """Get top content from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__top(page_number, page_multiplier)

    def popular_movies(self, page_number, page_multiplier=1):
        """Get popular movies from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__popular_movies(page_number, page_multiplier)

    def top_movies(self, page_number, page_multiplier=1):
        """Get top movies from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__top_movies(page_number, page_multiplier)

    def popular_tv(self, page_number, page_multiplier=1):
        """Get popular TV from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__popular_tv(page_number, page_multiplier)

    def top_tv(self, page_number, page_multiplier=1):
        """Get top TV from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__top_tv(page_number, page_multiplier)

    def discover_by_filter(self, content_type, **kwargs):
        """Filter by keywords or any other TMDB filter capable arguements.
        (see tmdbsimple discover.movie and discover.tv)

        Args:
            content_type: String containing "movie" or "tv".
            # Additional kwargs #
            keyword: A single String or a List of strings.
            _______: Any other values supported by tmdbsimple discover.movie or discover.tv.
        """
        try:
            if kwargs.__contains__("keyword"):
                # Convert all keywords to IDs
                keyword_ids = self.__keywords_to_ids(kwargs["keyword"])
                if keyword_ids is not None:
                    kwargs["with_keywords"] = keyword_ids

                # Remove keyword strings (invalid parameters)
                kwargs.__delitem__("keyword")

            # Perform a discovery search for a movie
            if content_type.lower() == "movie":
                return cache.handler(
                    "discover movies by filter",
                    page_key=str(kwargs),
                    function=tmdb.Discover().movie,
                    cache_duration=DISCOVER_BY_FILTER_CACHE_TIMEOUT,
                    kwargs=kwargs,
                )

            # Perform a discovery search for a TV show
            if content_type.lower() == "tv":
                return cache.handler(
                    "discover tv by filter",
                    page_key=str(kwargs),
                    function=tmdb.Discover().tv,
                    cache_duration=DISCOVER_BY_FILTER_CACHE_TIMEOUT,
                    kwargs=kwargs,
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in discover().",
                log.WARNING,
                _logger,
            )

        except:
            log.handler("Failed to discover!", log.ERROR, _logger)

    def similar_and_recommended(self, tmdb_id, content_type):
        """Merges the results of similar and recommended.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
        """
        try:
            thread_list = []
            merged_results = None

            # Get recommended page one
            recommend_page_one = self.__recommended(tmdb_id, content_type, 1)

            # Gather additional recommended pages
            if recommend_page_one and recommend_page_one["total_pages"] > 1:
                for page_number in range(2, recommend_page_one["total_pages"]):
                    if page_number <= MAX_RECOMMENDED_PAGES:
                        thread = ReturnThread(
                            target=self.__recommended,
                            args=[tmdb_id, content_type, page_number],
                        )
                        thread.start()
                        thread_list.append(thread)

            # Get similar page one
            similar_page_one = self.__similar(tmdb_id, content_type, 1)

            # Gather up additional similar pages
            if similar_page_one and similar_page_one["total_pages"] > 1:
                for page_number in range(2, similar_page_one["total_pages"]):
                    if page_number <= MAX_SIMILAR_PAGES:
                        thread = ReturnThread(
                            target=self.__similar,
                            args=[tmdb_id, content_type, page_number],
                        )
                        thread.start()
                        thread_list.append(thread)

            # Merge page one while waiting for the others to fetch
            if recommend_page_one and similar_page_one:
                merged_results = self.__merge_results(
                    recommend_page_one, similar_page_one
                )
            # Either similar or recommended didn't have anything in them.
            else:
                merged_results = (
                    recommend_page_one if recommend_page_one else similar_page_one
                )

            if merged_results:
                # Wait for all the threads to complete and merge them in
                for thread in thread_list:
                    merged_results = self.__merge_results(merged_results, thread.join())

                self.determine_id_validity(merged_results)

                # Shuffle and return
                return self.__shuffle_results(merged_results)

        except:
            log.handler(
                "Failed to obtain merged Similar and Recommended!",
                log.ERROR,
                _logger,
            )
            return {}

    def collections(self, collection_id):
        """Obtains items in the collection of a given TMDB Collection ID.

        Args:
            collection_id: An Integer or String containing the TMDB Collection ID.
        """
        try:
            return cache.handler(
                "get collection by id",
                page_key=collection_id,
                function=tmdb.Collections(collection_id).info,
                cache_duration=COLLECTION_CACHE_TIMEOUT,
            )

        except:
            log.handler(
                "Failed to obtain collection with ID " + str(collection_id) + "!",
                log.ERROR,
                _logger,
            )

    def get_by_tmdb_id(self, tmdb_id, content_type, obtain_extras=True):
        """Obtains a movie or series given a TMDB ID.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
        """
        # Searches for content based on TMDB ID
        try:
            # Obtain extras if needed
            if obtain_extras:
                extras = "reviews,keywords,videos,credits,images"
            else:
                extras = None

            # Obtain a movie by ID
            if content_type.lower() == "movie":
                return cache.handler(
                    "get movie by tmdb id",
                    page_key=tmdb_id,
                    function=tmdb.Movies(tmdb_id).info,
                    cache_duration=GET_BY_TMDB_ID_CACHE_TIMEOUT,
                    kwargs={"append_to_response": extras},
                )

            # Obtain a TV show by ID
            if content_type.lower() == "tv":
                return cache.handler(
                    "get tv by tmdb id",
                    page_key=tmdb_id,
                    function=tmdb.TV(tmdb_id).info,
                    cache_duration=GET_BY_TMDB_ID_CACHE_TIMEOUT,
                    kwargs={"append_to_response": extras},
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in get_by_id().",
                log.WARNING,
                _logger,
            )

        except:
            log.handler(
                "Failed to obtain content by ID!",
                log.ERROR,
                _logger,
            )

    def get_by_tvdb_id(self, tvdb_id):
        """Converts get a TMDB show by a TVDB ID.

        Args:
            id: An Integer or String containing the TVDB ID.
        """
        try:
            return cache.handler(
                "get tv by tvdb id",
                page_key=tvdb_id,
                function=tmdb.Find(tvdb_id).info,
                cache_duration=GET_BY_TVDB_ID_CACHE_TIMEOUT,
                kwargs={"external_source": "tvdb_id"},
            )

        except:
            log.handler(
                "Failed to obtain content with TVDB ID " + str(tvdb_id) + "!",
                log.ERROR,
                _logger,
            )

    def get_external_ids(self, tmdb_id, content_type):
        """Gets all external IDs given a TMDB ID.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
        """
        try:
            # Obtain a movie's external IDs
            if content_type.lower() == "movie":
                return cache.handler(
                    "get movie external ids",
                    page_key=tmdb_id,
                    function=tmdb.Movies(tmdb_id).external_ids,
                    cache_duration=EXTERNAL_ID_CACHE_TIMEOUT,
                )

            # Obtain a TV show's external IDs
            if content_type.lower() == "tv":
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

    def get_genres(self, content_type):
        """Gets all available TMDB genres and genre IDs.

        Args:
            content_type: String containing "movie" or "tv".
        """
        try:
            # Obtain a movie's genres
            if content_type.lower() == "movie":
                return cache.handler(
                    "get all movie genres",
                    function=tmdb.Genres().movie_list,
                    cache_duration=GET_GENRES_CACHE_TIMEOUT,
                )

            # Obtain a TV show's genres
            if content_type.lower() == "tv":
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

    def is_anime(self, tmdb_id, content_type):
        """Checks if a TMDB ID can be considered Anime.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
        """
        try:
            # TV: Obtain the keywords for a specific ID
            if content_type.lower() == "tv":
                return cache.handler(
                    "is tv anime",
                    function=self.__is_tv_anime,
                    cache_duration=IS_ANIME_CACHE_TIMEOUT,
                    args=[tmdb_id],
                )

            # Movies: Obtain the keywords for a specific ID
            if content_type.lower() == "movie":
                return cache.handler(
                    "is movie anime",
                    function=self.__is_movie_anime,
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

    def determine_id_validity(self, tmdb_response):
        """Determine if a movie has a TMDB ID, and if TV has a TVDBID.
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

    # Private Class Methods
    def __all(self, page_number, page_multiplier):
        """Cacheable part of all()"""
        # Merge popular_movies, popular_tv, top_movies, and top_tv results together
        function_list = [
            self.__popular_movies,
            self.__popular_tv,
            self.__top_movies,
            self.__top_tv,
        ]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self.__shuffle_results(self.__merge_results(*results))

    def __tv(self, page_number, page_multiplier):
        """Cacheable part of tv()"""
        # Merge popular_tv and top_tv results together
        function_list = [self.__popular_tv, self.__top_tv]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self.__shuffle_results(self.__merge_results(*results))

    def __movies(self, page_number, page_multiplier):
        """Cacheable part of movies()"""
        # Merge popular_movies and top_movies results together
        function_list = [self.__popular_movies, self.__top_movies]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self.__shuffle_results(self.__merge_results(*results))

    def __popular(self, page_number, page_multiplier):
        """Cacheable part of popular()"""
        # Merge popular_movies and popular_tv results together
        function_list = [self.__popular_movies, self.__popular_tv]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self.__shuffle_results(self.__merge_results(*results))

    def __top(self, page_number, page_multiplier):
        """Cacheable part of top()"""
        # Merge top_movies and top_tv results together
        function_list = [self.__top_movies, self.__top_tv]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self.__shuffle_results(self.__merge_results(*results))

    def __popular_movies(self, page_number, page_multiplier):
        """Cacheable part of popular_movies()"""
        # Obtain disovery results through the movie.popular function. Store results in cache.
        return self.__multi_page_fetch(
            "discover popular movies",
            tmdb.Movies().popular,
            page_number,
            page_multiplier,
        )

    def __top_movies(self, page_number, page_multiplier):
        """Cacheable part of top_movies()"""
        # Obtain disovery results through the movie.top_rated function. Store results in cache.
        return self.__multi_page_fetch(
            "discover top movies",
            tmdb.Movies().top_rated,
            page_number,
            page_multiplier,
        )

    def __popular_tv(self, page_number, page_multiplier):
        """Cacheable part of popular_tv()"""
        # Obtain disovery results through the tv.popular function. Store results in cache.
        return self.__multi_page_fetch(
            "discover popular tv", tmdb.TV().popular, page_number, page_multiplier
        )

    def __top_tv(self, page_number, page_multiplier):
        """Cacheable part of top_tv()"""
        # Obtain disovery results through the tv.top_rated function. Store results in cache.
        return self.__multi_page_fetch(
            "discover top tv", tmdb.TV().top_rated, page_number, page_multiplier
        )

    def __recommended(self, tmdb_id, content_type, page_number):
        """Obtains recommendations given a TMDB ID.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
            page_number: An Integer that is the page number to return.
        """
        try:
            if content_type.lower() == "movie":
                return cache.handler(
                    "discover recommended movies",
                    page_key=str(tmdb_id) + "page" + str(page_number),
                    function=tmdb.Movies(tmdb_id).recommendations,
                    cache_duration=RECOMMENDED_CACHE_TIMEOUT,
                    kwargs={
                        "language": LANGUAGE,
                        "page": page_number,
                    },
                )

            if content_type.lower() == "tv":
                return cache.handler(
                    "discover recommended tv",
                    page_key=str(tmdb_id) + "page" + str(page_number),
                    function=tmdb.TV(tmdb_id).recommendations,
                    cache_duration=RECOMMENDED_CACHE_TIMEOUT,
                    kwargs={
                        "language": LANGUAGE,
                        "page": page_number,
                    },
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in recommend().",
                log.WARNING,
                _logger,
            )

        except:
            log.handler(
                "Failed to obtain recommendations!",
                log.ERROR,
                _logger,
            )

    def __similar(self, tmdb_id, content_type, page_number):
        """Obtains similar content given a TMDB ID.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
            page_number: An Integer that is the page number to return.
        """
        try:
            if content_type.lower() == "movie":
                return cache.handler(
                    "discover similar movies",
                    page_key=str(tmdb_id) + "page" + str(page_number),
                    function=tmdb.Movies(tmdb_id).similar_movies,
                    cache_duration=SIMILAR_CACHE_TIMEOUT,
                    kwargs={
                        "language": LANGUAGE,
                        "page": page_number,
                    },
                )

            if content_type.lower() == "tv":
                return cache.handler(
                    "discover similar tv",
                    page_key=str(tmdb_id) + "page" + str(page_number),
                    function=tmdb.TV(tmdb_id).similar,
                    cache_duration=SIMILAR_CACHE_TIMEOUT,
                    kwargs={
                        "language": LANGUAGE,
                        "page": page_number,
                    },
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in similar().",
                log.WARNING,
                _logger,
            )

        except:
            log.handler(
                "Failed to obtain similar content!",
                log.ERROR,
                _logger,
            )

    def __multi_page_fetch(self, cache_name, function, page_number, page_multiplier):
        """Obtains multiple pages of results at once via threads."""
        total_pages = page_number * page_multiplier
        thread_list = []
        for subtractor in range(0, page_multiplier):
            thread = ReturnThread(
                target=cache.handler,
                args=[
                    cache_name,
                ],
                kwargs={
                    "function": function,
                    "page_key": total_pages - subtractor,
                    "cache_duration": POPULAR_AND_TOP_CACHE_TIMEOUT,
                    "kwargs": {"page": total_pages - subtractor, "language": LANGUAGE},
                },
            )
            thread.start()
            thread_list.append(thread)

        # Merge together these pages
        merged_results = thread_list[0].join()
        thread_list.remove(thread_list[0])
        for thread in thread_list:
            merged_results = self.__merge_results(merged_results, thread.join())

        # Determine if TV has a TVDB ID (required for Sonarr)
        self.determine_id_validity(merged_results)

        return merged_results

    def __keywords_to_ids(self, keywords):
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

    def __is_tv_anime(self, tmdb_id):
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

    def __is_movie_anime(self, tmdb_id):
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

    def __determine_id_validity(self, card):
        """Threaded executable for determine_id_validity()"""
        try:
            external_id_results = self.get_external_ids(card["id"], "tv")
            if external_id_results["tvdb_id"] is not None:
                card["conreq_valid_id"] = True
                card["tvdb_id"] = external_id_results["tvdb_id"]
        except:
            pass

    def __merge_results(self, *args):
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

            return self.__remove_duplicate_results(merged_results)

        except:
            log.handler(
                "Failed to merge results!",
                log.ERROR,
                _logger,
            )
            return {}

    def __shuffle_results(self, query):
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

    def __remove_duplicate_results(self, query):
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
    def __shuffled_page_numbers():
        """Cacheable part of shuffled_page_numbers()"""
        temp_list = [*range(1, MAX_SHUFFLED_PAGES + 1)]
        shuffle(temp_list)
        return dict(enumerate(temp_list, start=1))
