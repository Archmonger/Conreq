"""Conreq Content Discovery: Searches TMDB for content."""
from random import shuffle

import tmdbsimple as tmdb
from conreq.utils import cache, log
from conreq.utils.generic import (
    ReturnThread,
    is_key_value_in_list,
    obtain_key_from_cache_key,
    threaded_execution,
)

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
GET_GENRES_CACHE_TIMEOUT = 30 * 24 * 60 * 60
RECOMMENDED_CACHE_TIMEOUT = 14 * 24 * 60 * 60
SIMILAR_CACHE_TIMEOUT = 14 * 24 * 60 * 60
POPULAR_AND_TOP_CACHE_TIMEOUT = 3 * 24 * 60 * 60
KEYWORDS_TO_IDS_CACHE_TIMEOUT = 30 * 24 * 60 * 60
SHUFFLED_PAGE_CACHE_TIMEOUT = 1 * 24 * 60 * 60


class ContentDiscovery:
    """Discovers top, trending, and recommended content using TMDB as the backend.
    >>> Args:
        tmdb_api_key: String containing the TMDB API key.
    """

    def __init__(self):
        # TMDB API key is safe to hard-code. It can only access publicly available data.
        tmdb.API_KEY = "112fd4c96274603f68620c78067d5422"

        # Creating a logger (for log files)
        self.__logger = log.get_logger(__name__)

    # Public class methods
    def all(self, page_number, page_multiplier=1):
        """Get top and popular content from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        # Shuffle the order of the first N many pages for randomized discovery
        if page_number <= MAX_SHUFFLED_PAGES:
            page = cache.handler(
                "all page numbers cache",
                function=self.__shuffled_page_numbers,
                cache_duration=SHUFFLED_PAGE_CACHE_TIMEOUT,
            )[page_number]
        else:
            page = page_number

        return cache.handler(
            "all cache",
            self.__all,
            page,
            False,
            SHUFFLED_PAGE_CACHE_TIMEOUT,
            page,
            page_multiplier,
        )

    def tv(self, page_number, page_multiplier=1):
        """Get top and popular TV from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        # Shuffle the order of the first N many pages for randomized discovery
        if page_number <= MAX_SHUFFLED_PAGES:
            page = cache.handler(
                "tv page numbers cache",
                function=self.__shuffled_page_numbers,
                cache_duration=SHUFFLED_PAGE_CACHE_TIMEOUT,
            )[page_number]
        else:
            page = page_number

        return cache.handler(
            "tv cache",
            self.__tv,
            page,
            False,
            SHUFFLED_PAGE_CACHE_TIMEOUT,
            page,
            page_multiplier,
        )

    def movies(self, page_number, page_multiplier=1):
        """Get top and popular TV from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        # Shuffle the order of the first N many pages for randomized discovery
        if page_number <= MAX_SHUFFLED_PAGES:
            page = cache.handler(
                "movie page numbers cache",
                function=self.__shuffled_page_numbers,
                cache_duration=SHUFFLED_PAGE_CACHE_TIMEOUT,
            )[page_number]
        else:
            page = page_number

        return cache.handler(
            "movie cache",
            self.__movies,
            page,
            False,
            SHUFFLED_PAGE_CACHE_TIMEOUT,
            page,
            page_multiplier,
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
                    "discover movie cache",
                    function=tmdb.Discover().movie,
                    page_key=str(kwargs),
                    cache_duration=DISCOVER_BY_FILTER_CACHE_TIMEOUT,
                    **kwargs,
                )

            # Perform a discovery search for a TV show
            if content_type.lower() == "tv":
                return cache.handler(
                    "discover tv cache",
                    function=tmdb.Discover().tv,
                    page_key=str(kwargs),
                    cache_duration=DISCOVER_BY_FILTER_CACHE_TIMEOUT,
                    **kwargs,
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in discover().",
                log.WARNING,
                self.__logger,
            )
            return {}

        except:
            log.handler("Failed to discover!", log.ERROR, self.__logger)
            return {}

    def similar_and_recommended(self, tmdb_id, content_type):
        """Merges the results of similar and recommended.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
        """
        try:
            thread_list = []

            # Get recommended page one
            recommend_page_one = self.__recommended(tmdb_id, content_type, 1)

            # Gather additional recommended pages
            if recommend_page_one["total_pages"] > 1:
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
            if similar_page_one["total_pages"] > 1:
                for page_number in range(2, similar_page_one["total_pages"]):
                    if page_number <= MAX_SIMILAR_PAGES:
                        thread = ReturnThread(
                            target=self.__similar,
                            args=[tmdb_id, content_type, page_number],
                        )
                        thread.start()
                        thread_list.append(thread)

            # Merge results of the first page of similar and recommended
            merged_results = self.__merge_results(recommend_page_one, similar_page_one)

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
                self.__logger,
            )
            return {}

    def collections(self, collection_id):
        """Obtains items in the collection of a given TMDB Collection ID.

        Args:
            collection_id: An Integer or String containing the TMDB Collection ID.
        """
        return tmdb.Collections(collection_id).info()

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
                    "movie by id cache",
                    function=tmdb.Movies(tmdb_id).info,
                    page_key=tmdb_id,
                    cache_duration=GET_BY_TMDB_ID_CACHE_TIMEOUT,
                    append_to_response=extras,
                )

            # Obtain a TV show by ID
            if content_type.lower() == "tv":
                return cache.handler(
                    "tv by id cache",
                    function=tmdb.TV(tmdb_id).info,
                    page_key=tmdb_id,
                    cache_duration=GET_BY_TMDB_ID_CACHE_TIMEOUT,
                    append_to_response=extras,
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in get_by_id().",
                log.WARNING,
                self.__logger,
            )
            return {}

        except:
            log.handler(
                "Failed to obtain content by ID!",
                log.ERROR,
                self.__logger,
            )
            return {}

    def get_by_tvdb_id(self, tvdb_id):
        """Converts TVDB ID to TMDB ID.

        Args:
            id: An Integer or String containing the TMDB ID.
        """
        # TODO: Add caching
        try:
            return tmdb.Find(tvdb_id).info(external_source="tvdb_id")

        except:
            log.handler(
                "Failed to obtain content with TVDB ID " + str(tvdb_id) + "!",
                log.ERROR,
                self.__logger,
            )
            return None

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
                    "movie external id cache",
                    function=tmdb.Movies(tmdb_id).external_ids,
                    page_key=tmdb_id,
                    cache_duration=EXTERNAL_ID_CACHE_TIMEOUT,
                )

            # Obtain a TV show's external IDs
            if content_type.lower() == "tv":
                return cache.handler(
                    "tv external id cache",
                    function=tmdb.TV(tmdb_id).external_ids,
                    page_key=tmdb_id,
                    cache_duration=EXTERNAL_ID_CACHE_TIMEOUT,
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in get_external_ids().",
                log.WARNING,
                self.__logger,
            )
            return {}

        except:
            log.handler(
                "Failed to obtain external ID!",
                log.ERROR,
                self.__logger,
            )
            return {}

    def get_genres(self, content_type):
        """Gets all available TMDB genres and genre IDs.

        Args:
            content_type: String containing "movie" or "tv".
        """
        try:
            # Obtain a movie's genres
            if content_type.lower() == "movie":
                return cache.handler(
                    "movie genres cache",
                    function=tmdb.Genres().movie_list,
                    cache_duration=GET_GENRES_CACHE_TIMEOUT,
                )

            # Obtain a TV show's genres
            if content_type.lower() == "tv":
                return cache.handler(
                    "movie genres cache",
                    function=tmdb.Genres().tv_list,
                    cache_duration=GET_GENRES_CACHE_TIMEOUT,
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in get_genres().",
                log.WARNING,
                self.__logger,
            )
            return {}

        except:
            log.handler(
                "Failed to obtain genres!",
                log.ERROR,
                self.__logger,
            )
            return {}

    def is_anime(self, tmdb_id, content_type):
        """Checks if a TMDB ID can be considered Anime.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
        """
        # TODO: Add caching
        try:
            # TV: Obtain the keywords for a specific ID
            if content_type.lower() == "tv":
                api_results = tmdb.TV(tmdb_id).keywords()

                # Check if the content contains Keyword: Anime
                if is_key_value_in_list("name", "anime", api_results["results"]):
                    log.handler(
                        str(tmdb_id) + " is anime.",
                        log.INFO,
                        self.__logger,
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
                            self.__logger,
                        )
                        return True

            # Movies: Obtain the keywords for a specific ID
            elif content_type.lower() == "movie":
                api_results = tmdb.Movies(tmdb_id).keywords()

                # Check if the content contains Keyword: Anime
                if is_key_value_in_list("name", "anime", api_results["keywords"]):
                    log.handler(
                        str(tmdb_id) + " is anime.",
                        log.INFO,
                        self.__logger,
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
                            self.__logger,
                        )
                        return True

            # Content Type was invalid
            else:
                log.handler(
                    "Invalid content_type " + str(content_type) + " in is_anime().",
                    log.WARNING,
                    self.__logger,
                )

            log.handler(
                str(tmdb_id) + " is not anime.",
                log.INFO,
                self.__logger,
            )

            # None of our methods detected this content as Anime
            return False

        except:
            log.handler(
                "Failed to check if content is anime!",
                log.ERROR,
                self.__logger,
            )
            return False

    def determine_id_validity(self, tmdb_response):
        # Needed because TVDB IDs are required for Sonarr
        external_id_multi_fetch = {}

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
                    "card": result,
                }

            # TMDB Movie card
            elif result.__contains__("title"):
                result["conreq_valid_id"] = True

        # Grab external IDs if needed
        external_id_cache_results = cache.handler(
            "tv external id cache",
            function=external_id_multi_fetch,
            cache_duration=EXTERNAL_ID_CACHE_TIMEOUT,
        )

        # Set the tvdb_id, and if it exists then this TMDB card has a valid ID
        if external_id_cache_results is not None:
            for cache_key, external_id_results in external_id_cache_results.items():
                key = obtain_key_from_cache_key(cache_key)
                try:
                    if external_id_results["tvdb_id"] is not None:
                        external_id_multi_fetch[key]["card"]["conreq_valid_id"] = True
                        external_id_multi_fetch[key]["card"][
                            "tvdb_id"
                        ] = external_id_results["tvdb_id"]

                except:
                    pass

    # Private Class Methods
    def __all(self, page_number, page_multiplier):
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
        # Merge popular_tv and top_tv results together
        function_list = [self.__popular_tv, self.__top_tv]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self.__shuffle_results(self.__merge_results(*results))

    def __movies(self, page_number, page_multiplier):
        # Merge popular_movies and top_movies results together
        function_list = [self.__popular_movies, self.__top_movies]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self.__shuffle_results(self.__merge_results(*results))

    def __popular(self, page_number, page_multiplier):
        # Merge popular_movies and popular_tv results together
        function_list = [self.__popular_movies, self.__popular_tv]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self.__shuffle_results(self.__merge_results(*results))

    def __top(self, page_number, page_multiplier):
        # Merge top_movies and top_tv results together
        function_list = [self.__top_movies, self.__top_tv]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self.__shuffle_results(self.__merge_results(*results))

    def __popular_movies(self, page_number, page_multiplier):
        # Obtain disovery results through the movie.popular function. Store results in cache.
        return self.__multi_page_fetch(
            "popular movie cache",
            tmdb.Movies().popular,
            page_number,
            "movie",
            page_multiplier,
        )

    def __top_movies(self, page_number, page_multiplier):
        # Obtain disovery results through the movie.top_rated function. Store results in cache.
        return self.__multi_page_fetch(
            "top movie cache",
            tmdb.Movies().top_rated,
            page_number,
            "movie",
            page_multiplier,
        )

    def __popular_tv(self, page_number, page_multiplier):
        # Obtain disovery results through the tv.popular function. Store results in cache.
        return self.__multi_page_fetch(
            "popular tv cache", tmdb.TV().popular, page_number, "tv", page_multiplier
        )

    def __top_tv(self, page_number, page_multiplier):
        # Obtain disovery results through the tv.top_rated function. Store results in cache.
        return self.__multi_page_fetch(
            "top tv cache", tmdb.TV().top_rated, page_number, "tv", page_multiplier
        )

    def __recommended(self, tmdb_id, content_type, page_number):
        """Obtains recommendations given a TMDB ID.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
            page_number: An Integer that is the page number to return.
        """
        # Performs a recommended search
        try:
            if content_type.lower() == "movie":
                return cache.handler(
                    "movie recommendations cache",
                    function=tmdb.Movies(tmdb_id).recommendations,
                    page_key=str(tmdb_id) + "page" + str(page_number),
                    cache_duration=RECOMMENDED_CACHE_TIMEOUT,
                    page=page_number,
                    language=LANGUAGE,
                )

            if content_type.lower() == "tv":
                return cache.handler(
                    "tv recommendations cache",
                    function=tmdb.TV(tmdb_id).recommendations,
                    page_key=str(tmdb_id) + "page" + str(page_number),
                    cache_duration=RECOMMENDED_CACHE_TIMEOUT,
                    page=page_number,
                    language=LANGUAGE,
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in recommend().",
                log.WARNING,
                self.__logger,
            )
            return {}

        except:
            log.handler(
                "Failed to obtain recommendations!",
                log.ERROR,
                self.__logger,
            )
            return {}

    def __similar(self, tmdb_id, content_type, page_number):
        """Obtains similar content given a TMDB ID.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
            page_number: An Integer that is the page number to return.
        """
        # Searches for similar content based on id
        try:
            if content_type.lower() == "movie":
                return cache.handler(
                    "movie similar cache",
                    function=tmdb.Movies(tmdb_id).similar_movies,
                    page_key=str(tmdb_id) + "page" + str(page_number),
                    cache_duration=SIMILAR_CACHE_TIMEOUT,
                    page=page_number,
                    language=LANGUAGE,
                )

            if content_type.lower() == "tv":
                return cache.handler(
                    "tv similar cache",
                    function=tmdb.TV(tmdb_id).similar,
                    page_key=str(tmdb_id) + "page" + str(page_number),
                    cache_duration=SIMILAR_CACHE_TIMEOUT,
                    page=page_number,
                    language=LANGUAGE,
                )

            # Content Type was invalid
            log.handler(
                "Invalid content_type " + str(content_type) + " in similar().",
                log.WARNING,
                self.__logger,
            )
            return {}

        except:
            log.handler(
                "Failed to obtain similar content!",
                log.ERROR,
                self.__logger,
            )
            return {}

    def __multi_page_fetch(
        self, cache_name, function, page_number, content_type, page_multiplier
    ):
        # Obtain multiple pages of TMDB queries
        total_pages = page_number * page_multiplier
        thread_list = []
        for subtractor in range(0, page_multiplier):
            thread = ReturnThread(
                target=cache.handler,
                args=[
                    cache_name,
                    function,
                    total_pages - subtractor,
                    False,
                    POPULAR_AND_TOP_CACHE_TIMEOUT,
                ],
                kwargs={"page": total_pages - subtractor, "language": LANGUAGE},
            )
            thread.start()
            thread_list.append(thread)

        # Merge together these pages
        merged_results = thread_list[0].join()
        thread_list.remove(thread_list[0])
        for thread in thread_list:
            merged_results = self.__merge_results(merged_results, thread.join())

        # Set to valid ID to True, since tmdb is a valid source for Radarr.
        if content_type == "movie":
            for result in merged_results["results"]:
                result["conreq_valid_id"] = True

        # Determine if TV has a TVDB ID (required for Sonarr)
        self.determine_id_validity(merged_results)

        return merged_results

    def __keywords_to_ids(self, keywords):
        # Turn a keyword string or a list of keywords into a TMDB keyword ID number
        try:
            keyword_ids = []

            # A list of keywords was given
            if len(keywords) >= 1 and isinstance(keywords, list):
                for keyword in keywords:
                    # Perform a search
                    keyword_search = cache.handler(
                        "keyword to id cache",
                        function=tmdb.Search().keyword,
                        page_key=keyword,
                        cache_duration=KEYWORDS_TO_IDS_CACHE_TIMEOUT,
                        query=keyword,
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
                    "keyword to id cache",
                    function=tmdb.Search().keyword,
                    page_key=keywords,
                    cache_duration=KEYWORDS_TO_IDS_CACHE_TIMEOUT,
                    query=keywords,
                )["results"]

                for search_result in keyword_search:
                    # Find an exact match
                    if search_result["name"].lower() == keywords.lower():
                        # Return the keyword ID number
                        keyword_ids.append(search_result["id"])

            # User put in values in an improper format
            else:
                log.handler(
                    "Keyword(s) "
                    + str(keywords)
                    + " were provided in an improper format",
                    log.WARNING,
                    self.__logger,
                )
                return None

            # We managed to obtain at least one ID
            if len(keyword_ids) >= 1:
                return keyword_ids

            # We couldn't obtain any IDs
            log.handler(
                "Keyword(s) " + str(keywords) + " not found!",
                log.INFO,
                self.__logger,
            )
            return None

        except:
            log.handler(
                "Failed to obtain keyword!",
                log.ERROR,
                self.__logger,
            )
            return None

    def __merge_results(self, *args):
        # Merge multiple API results into one
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
                self.__logger,
            )
            return {}

    def __shuffle_results(self, query):
        # Shuffle API results
        try:
            shuffle(query["results"])
            return query

        except:
            log.handler(
                "Failed to shuffle results!",
                log.ERROR,
                self.__logger,
            )
            return {}

    def __remove_duplicate_results(self, query):
        # Removes duplicates from a dict
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
                        self.__logger,
                    )

            query["results"] = clean_results
            return query
        except:
            log.handler(
                "Failed to remove duplicate results!",
                log.ERROR,
                self.__logger,
            )
            return {}

    @staticmethod
    def __shuffled_page_numbers():
        temp_list = [*range(1, MAX_SHUFFLED_PAGES + 1)]
        shuffle(temp_list)
        return dict(enumerate(temp_list, start=1))


# Test driver code
# if __name__ == "__main__":
# content_discovery = ContentDiscovery()

# print("\n#### Discover All Test ####")
# pprint(content_discovery.all(1))
# print("\n#### Discover Top Test ####")
# pprint(content_discovery.top(1))
# print("\n#### Discover Top Movies Test ####")
# pprint(content_discovery.top_movies(1))
# print("\n#### Discover Top TV Test ####")
# pprint(content_discovery.top_tv(1))
# print("\n#### Discover Popular Test ####")
# pprint(content_discovery.popular(1))
# print("\n#### Discover Popular Movies Test ####")
# pprint(content_discovery.popular_movies(1))
# print("\n#### Discover Popular TV Test ####")
# pprint(content_discovery.popular_tv(1))
# print("\n#### TV External ID Test ####")
# pprint(content_discovery.get_external_ids(2222, "tv"))
# print("\n#### Movie External ID Test ####")
# pprint(content_discovery.get_external_ids(2222, "movie"))
# print("\n#### TVDB to TMDB Test ####")
# pprint(content_discovery.tvdb_id_to_tmdb("276562"))
# print("\n#### Discover Test ####")
# pprint(content_discovery.discover("tv", keyword=["anime", "japan"]))
# print("\n#### Recommend Test ####")
# pprint(content_discovery.recommend(45923, "tv", 1))
# print("\n#### Similar Test ####")
# pprint(content_discovery.similar(45923, "tv", 1))
# print("\n#### Check if TV is Anime Test ####")
# pprint(content_discovery.is_anime(63926, "tv"))
# print("\n#### Check if TV is Anime Test ####")
# pprint(content_discovery.is_anime(101010, "tv"))
# print("\n#### Check if Movie is Anime Test ####")
# pprint(content_discovery.is_anime(592350, "movie"))
# print("\n#### Check if Movie is Anime Test ####")
# pprint(content_discovery.is_anime(101010, "movie"))
# print("\n#### Get TV Genres Test ####")
# pprint(content_discovery.get_genres("tv"))
# print("\n#### Get Movie Genres Test ####")
# pprint(content_discovery.get_genres("movie"))
# print("\n#### Similar and Recommend Test ####")
# pprint(content_discovery.similar_and_recommended(45923, "tv"))
