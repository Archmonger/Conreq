"""Conreq Content Discovery: Searches TMDB for content."""
from random import shuffle

import tmdbsimple as tmdb
from conreq.core import cache, log
from conreq.core.generic_tools import is_key_value_in_list
from conreq.core.thread_helper import ReturnThread, threaded_execution

# TODO: Obtain these values from the database on init
ANIME_CHECK_FALLBACK = True
LANGUAGE = "en"
FETCH_MULTI_PAGE = 5


class ContentDiscovery:
    """Discovers top, trending, and recommended content using TMDB as the backend.
    >>> Args:
        tmdb_api_key: String containing the TMDB API key.
    """

    def __init__(self, tmdb_api_key):
        # Initialize the TMDB API library
        self.__tmdb_movies = tmdb.Movies()
        self.__tmdb_tv = tmdb.TV()
        self.__search = tmdb.Search()
        self.__discover = tmdb.Discover()
        self.__finder = tmdb.Find()
        self.__genres = tmdb.Genres()
        self.__collections = tmdb.Collections(id=0)
        # TODO: Obtain this value from the database on init
        tmdb.API_KEY = tmdb_api_key

        # Creating a logger (for log files)
        self.__logger = log.get_logger("Content Discovery")
        log.configure(self.__logger, log.DEBUG)

    # Exposed class methods
    def all(self, page_number):
        """Get top and popular content from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__shuffle_results(self.__all(page_number))

    def tv(self, page_number):
        """Get top and popular TV from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__shuffle_results(self.__tv(page_number))

    def movies(self, page_number):
        """Get top and popular TV from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__shuffle_results(self.__movies(page_number))

    def popular(self, page_number):
        """Get popular content from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__shuffle_results(self.__popular(page_number))

    def top(self, page_number):
        """Get top content from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__shuffle_results(self.__top(page_number))

    def popular_movies(self, page_number):
        """Get popular movies from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__shuffle_results(self.__popular_movies(page_number))

    def top_movies(self, page_number):
        """Get top movies from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__shuffle_results(self.__top_movies(page_number))

    def popular_tv(self, page_number):
        """Get popular TV from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__shuffle_results(self.__popular_tv(page_number))

    def top_tv(self, page_number):
        """Get top TV from TMDB.

        Args:
            page_number: An Integer that is the page number to return.
        """
        return self.__shuffle_results(self.__top_tv(page_number))

    def discover(self, content_type, **kwargs):
        """Filter by keywords.

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
                    self.__discover.movie,
                    str(kwargs),
                    **kwargs,
                )

            # Perform a discovery search for a TV show
            if content_type.lower() == "tv":
                return cache.handler(
                    "discover tv cache",
                    self.__discover.tv,
                    str(kwargs),
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

            # Gather up to 9 additional recommended pages
            for page_number in range(1, recommend_page_one["total_pages"]):
                if page_number <= 5:
                    thread = ReturnThread(
                        target=self.__recommended,
                        args=[tmdb_id, content_type, page_number],
                    )
                    thread.start()
                    thread_list.append(thread)

            # Get similar page one
            similar_page_one = self.__similar(tmdb_id, content_type, 1)

            # Gather up to 9 additional similar pages
            for page_number in range(1, similar_page_one["total_pages"]):
                if page_number <= 5:
                    thread = ReturnThread(
                        target=self.__similar, args=[tmdb_id, content_type, page_number]
                    )
                    thread.start()
                    thread_list.append(thread)

            # Merge results of the first page of similar and recommended
            merged_results = self.__merge_results(recommend_page_one, similar_page_one)

            # Wait for all the threads to complete and merge them in
            for thread in thread_list:
                merged_results = self.__merge_results(merged_results, thread.join())

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
        self.__collections.id = collection_id
        return self.__collections.info()

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
                self.__tmdb_movies.id = tmdb_id
                return cache.handler(
                    "movie by id cache",
                    self.__tmdb_movies.info,
                    tmdb_id,
                    append_to_response=extras,
                )

            # Obtain a TV show by ID
            if content_type.lower() == "tv":
                self.__tmdb_tv.id = tmdb_id
                return cache.handler(
                    "tv by id cache",
                    self.__tmdb_tv.info,
                    tmdb_id,
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
            self.__finder.id = tvdb_id
            return self.__finder.info(external_source="tvdb_id")

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
                self.__tmdb_movies.id = tmdb_id
                return cache.handler(
                    "movie external id cache",
                    self.__tmdb_movies.external_ids,
                    tmdb_id,
                )

            # Obtain a TV show's external IDs
            if content_type.lower() == "tv":
                self.__tmdb_tv.id = tmdb_id
                return cache.handler(
                    "tv external id cache",
                    self.__tmdb_tv.external_ids,
                    tmdb_id,
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
        """Gets all external IDs given a TMDB ID.

        Args:
            content_type: String containing "movie" or "tv".
        """
        try:
            # Obtain a movie's genres
            if content_type.lower() == "movie":
                return cache.handler(
                    "movie genres cache",
                    self.__genres.movie_list,
                    1,
                )

            # Obtain a TV show's genres
            if content_type.lower() == "tv":
                return cache.handler(
                    "movie genres cache",
                    self.__genres.tv_list,
                    1,
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
                self.__tmdb_tv.id = tmdb_id
                api_results = self.__tmdb_tv.keywords()

                # Check if the content contains Keyword: Anime
                if is_key_value_in_list(api_results["results"], "name", "anime"):
                    return True

                # Check if fallback method is enabled
                if ANIME_CHECK_FALLBACK:
                    tv_info = self.__tmdb_tv.info()
                    # Check if genere is Animation and Country is Japan
                    if (
                        is_key_value_in_list(tv_info["genres"], "name", "Animation")
                        and "JP" in tv_info["origin_country"]
                    ):
                        return True

            # Movies: Obtain the keywords for a specific ID
            elif content_type.lower() == "movie":
                self.__tmdb_movies.id = tmdb_id
                api_results = self.__tmdb_movies.keywords()

                # Check if the content contains Keyword: Anime
                if is_key_value_in_list(api_results["keywords"], "name", "anime"):
                    return True

                # Check if fallback method is enabled
                if ANIME_CHECK_FALLBACK:
                    movie_info = self.__tmdb_movies.info()

                    # Check if genere is Animation and Country is Japan
                    if is_key_value_in_list(
                        movie_info["genres"], "name", "Animation"
                    ) and is_key_value_in_list(
                        movie_info["production_countries"], "iso_3166_1", "JP"
                    ):
                        return True

            # Content Type was invalid
            else:
                log.handler(
                    "Invalid content_type " + str(content_type) + " in is_anime().",
                    log.WARNING,
                    self.__logger,
                )

            log.handler(
                "The " + str(content_type) + " " + str(tmdb_id) + " is not anime.",
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

    # Private Class Methods
    def __all(self, page_number):
        # Merge popular_movies, popular_tv, top_movies, and top_tv results together
        function_list = [
            self.__popular_movies,
            self.__popular_tv,
            self.__top_movies,
            self.__top_tv,
        ]
        results = threaded_execution(function_list, [page_number])
        return self.__merge_results(*results)

    def __tv(self, page_number):
        # Merge popular_tv and top_tv results together
        function_list = [self.__popular_tv, self.__top_tv]
        results = threaded_execution(function_list, [page_number])
        return self.__merge_results(*results)

    def __movies(self, page_number):
        # Merge popular_movies and top_movies results together
        function_list = [self.__popular_movies, self.__top_movies]
        results = threaded_execution(function_list, [page_number])
        return self.__merge_results(*results)

    def __popular(self, page_number):
        # Merge popular_movies and popular_tv results together
        function_list = [self.__popular_movies, self.__popular_tv]
        results = threaded_execution(function_list, [page_number])
        return self.__merge_results(*results)

    def __top(self, page_number):
        # Merge top_movies and top_tv results together
        function_list = [self.__top_movies, self.__top_tv]
        results = threaded_execution(function_list, [page_number])
        return self.__merge_results(*results)

    def __popular_movies(self, page_number):
        # Obtain disovery results through the movie.popular function. Store results in cache.
        return self.__threaded_multi_page_cached(
            "popular movie cache",
            self.__tmdb_movies.popular,
            page_number,
            "movie",
        )

    def __top_movies(self, page_number):
        # Obtain disovery results through the movie.top_rated function. Store results in cache.
        return self.__threaded_multi_page_cached(
            "top movie cache",
            self.__tmdb_movies.top_rated,
            page_number,
            "movie",
        )

    def __popular_tv(self, page_number):
        # Obtain disovery results through the tv.popular function. Store results in cache.
        return self.__threaded_multi_page_cached(
            "popular tv cache",
            self.__tmdb_tv.popular,
            page_number,
            "tv",
        )

    def __top_tv(self, page_number):
        # Obtain disovery results through the tv.top_rated function. Store results in cache.
        return self.__threaded_multi_page_cached(
            "top tv cache",
            self.__tmdb_tv.top_rated,
            page_number,
            "tv",
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
                self.__tmdb_movies.id = tmdb_id
                return cache.handler(
                    "movie recommendations cache",
                    self.__tmdb_movies.recommendations,
                    str(tmdb_id) + "page" + str(page_number),
                    page=page_number,
                    language=LANGUAGE,
                )

            if content_type.lower() == "tv":
                self.__tmdb_tv.id = tmdb_id
                return cache.handler(
                    "tv recommendations cache",
                    self.__tmdb_tv.recommendations,
                    str(tmdb_id) + "page" + str(page_number),
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
                self.__tmdb_movies.id = tmdb_id
                return cache.handler(
                    "movie similar cache",
                    self.__tmdb_movies.similar_movies,
                    str(tmdb_id) + "page" + str(page_number),
                    page=page_number,
                    language=LANGUAGE,
                )

            if content_type.lower() == "tv":
                self.__tmdb_tv.tmdb_id = tmdb_id
                return cache.handler(
                    "tv similar cache",
                    self.__tmdb_tv.similar,
                    str(tmdb_id) + "page" + str(page_number),
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

    def __threaded_multi_page_cached(
        self,
        cache_name,
        function,
        page_number,
        content_type,
    ):
        # Obtain multiple pages of TMDB queries
        total_pages = page_number * FETCH_MULTI_PAGE
        thread_list = []
        for subtractor in range(0, FETCH_MULTI_PAGE):
            thread = ReturnThread(
                target=cache.handler,
                args=[
                    cache_name,
                    function,
                    total_pages - subtractor,
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
        elif content_type == "tv":
            thread_list = []
            for result in merged_results["results"]:
                thread = ReturnThread(
                    target=self.get_external_ids,
                    args=[
                        result["id"],
                        content_type,
                    ],
                )
                thread.start()
                thread_list.append(thread)

            # Valid ID defaults to false
            for result in merged_results["results"]:
                result["conreq_valid_id"] = False

            # Set the external IDs
            for index, thread in enumerate(thread_list):
                current_result = merged_results["results"][index]
                current_result["external_ids"] = thread.join()

                # If it has a valid external id, set conreq_valid_id to True
                try:
                    if current_result["external_ids"]["tvdb_id"] is not None:
                        current_result["conreq_valid_id"] = True
                except:
                    pass

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
                        self.__search.keyword,
                        keyword,
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
                    self.__search.keyword,
                    keywords,
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


# Test driver code
if __name__ == "__main__":
    content_discovery = ContentDiscovery("x")

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
