"""Conreq Content Discovery: Searches TMDB for content."""
import tmdbsimple as tmdb
from conreq.utils import cache, log
from conreq.utils.multiprocessing import ReturnThread, threaded_execution

from .tmdb_base import (
    COLLECTION_CACHE_TIMEOUT,
    GET_BY_TMDB_ID_CACHE_TIMEOUT,
    GET_BY_TVDB_ID_CACHE_TIMEOUT,
    LANGUAGE,
    MAX_RECOMMENDED_PAGES,
    MAX_SHUFFLED_PAGES,
    PERSON_CACHE_TIMEOUT,
    RECOMMENDED_CACHE_TIMEOUT,
    SHUFFLED_PAGE_CACHE_TIMEOUT,
    SIMILAR_CACHE_TIMEOUT,
    Base,
    _timezone,
)
from .tmdb_preset_filters import movie_filters, tv_filters

_logger = log.get_logger(__name__)


class ContentDiscovery(Base):
    """Discovers top, trending, and recommended content using TMDB as the backend."""

    # Public class methods
    def all(self, page_number, page_multiplier=1):
        """Get top and popular TV/Movies from TMDB."""
        # Shuffle the order of the first N many pages for randomized discovery
        if page_number <= MAX_SHUFFLED_PAGES:
            page = cache.handler(
                "discover all page numbers",
                function=self._shuffled_page_numbers,
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
        """Get top and popular TV from TMDB."""
        # Shuffle the order of the first N many pages for randomized discovery
        if page_number <= MAX_SHUFFLED_PAGES:
            page = cache.handler(
                "discover tv page numbers",
                function=self._shuffled_page_numbers,
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
        """Get top and popular TV from TMDB."""
        # Shuffle the order of the first N many pages for randomized discovery
        if page_number <= MAX_SHUFFLED_PAGES:
            page = cache.handler(
                "discover movies page numbers",
                function=self._shuffled_page_numbers,
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
        """Get popular content from TMDB."""
        # Merge popular_movies and popular_tv results together
        function_list = [self.popular_movies, self.popular_tv]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self._shuffle_results(self._merge_results(*results))

    def top(self, page_number, page_multiplier=1):
        """Get top content from TMDB."""
        # Merge top_movies and top_tv results together
        function_list = [self.top_movies, self.top_tv]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self._shuffle_results(self._merge_results(*results))

    def popular_movies(self, page_number, page_multiplier=1):
        """Get popular movies from TMDB."""
        return self.discover_movie_by_filter(
            "popular",
            page_number,
            page_multiplier,
        )

    def top_movies(self, page_number, page_multiplier=1):
        """Get top movies from TMDB."""
        return self.discover_movie_by_filter(
            "top-rated",
            page_number,
            page_multiplier,
        )

    def popular_tv(self, page_number, page_multiplier=1):
        """Get popular TV from TMDB."""
        return self.discover_tv_by_filter("popular", page_number, page_multiplier)

    def top_tv(self, page_number, page_multiplier=1):
        """Get top TV from TMDB."""
        return self.discover_tv_by_filter("top-rated", page_number, page_multiplier)

    def discover_by_filter(
        self, filter_name, page_number, page_multiplier=1, add_values=(), **kwargs
    ):
        """Obtains TV/Movie results based on a predefined filter name."""
        function_list = [
            self.discover_movie_by_filter,
            self.discover_tv_by_filter,
        ]
        results = threaded_execution(
            function_list,
            [filter_name, page_number, page_multiplier, add_values],
            **kwargs,
        )

        # Shuffle the results on each page
        return self._shuffle_results(self._merge_results(*results))

    def discover_movie_by_filter(
        self, filter_name, page_number, page_multiplier=1, add_values=(), **kwargs
    ):
        """Obtains movie results based on a predefined filter name."""
        if filter_name == "custom":
            filter_params = kwargs
        else:
            filter_params = movie_filters(filter_name, slug=True, add_values=add_values)

        return self._set_content_attributes(
            "movie",
            self._multi_page_fetch(
                "discover filter " + filter_name + " movie",
                tmdb.Discover().movie,
                page_number,
                page_multiplier,
                timezone=_timezone,
                **filter_params,
            ),
        )

    def discover_tv_by_filter(
        self, filter_name, page_number, page_multiplier=1, add_values=(), **kwargs
    ):
        """Obtains TV results based on a predefined filter name."""
        if filter_name == "custom":
            filter_params = kwargs
        else:
            filter_params = tv_filters(filter_name, slug=True, add_values=add_values)

        return self._set_content_attributes(
            "tv",
            self._multi_page_fetch(
                "discover filter " + filter_name + " tv",
                tmdb.Discover().tv,
                page_number,
                page_multiplier,
                timezone=_timezone,
                **filter_params,
            ),
        )

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

            # There wasn't enough results in recommended, get one similar page
            if not recommend_page_one["total_pages"] > 1:
                thread = ReturnThread(
                    target=self.__similar,
                    args=[tmdb_id, content_type, 1],
                )
                thread.start()
                thread_list.append(thread)

            # Wait for all the threads to complete and merge them in
            merged_results = recommend_page_one
            for thread in thread_list:
                merged_results = self._merge_results(merged_results, thread.join())

            self.determine_id_validity(merged_results["results"])
            return merged_results

        except:
            log.handler(
                "Failed to obtain merged Similar and Recommended!",
                log.ERROR,
                _logger,
            )
            return {}

    def collections(self, collection_id):
        """Obtains items in the movie collection of a given TMDB Collection ID.

        Args:
            collection_id: An Integer or String containing the TMDB Collection ID.
        """
        try:
            return self._set_content_attributes(
                "movie",
                cache.handler(
                    "get collection by id",
                    page_key=collection_id,
                    function=tmdb.Collections(collection_id).info,
                    cache_duration=COLLECTION_CACHE_TIMEOUT,
                ),
            )

        except:
            log.handler(
                "Failed to obtain collection with ID " + str(collection_id) + "!",
                log.ERROR,
                _logger,
            )

    def person(self, person_id):
        """Obtain a person given a TMDB person ID.

        Args:
            id: An Integer or String containing the TMDB ID.
        """
        return self._set_content_attributes(
            None,
            cache.handler(
                "person",
                page_key=person_id,
                function=tmdb.People(person_id).info,
                cache_duration=PERSON_CACHE_TIMEOUT,
                kwargs={"append_to_response": "tv_credits,movie_credits"},
            ),
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
            if content_type == "movie":
                return self._set_content_attributes(
                    content_type,
                    cache.handler(
                        "get movie by tmdb id",
                        page_key=tmdb_id,
                        function=tmdb.Movies(tmdb_id).info,
                        cache_duration=GET_BY_TMDB_ID_CACHE_TIMEOUT,
                        kwargs={"append_to_response": extras},
                    ),
                )

            # Obtain a TV show by ID
            if content_type == "tv":
                return self._set_content_attributes(
                    content_type,
                    cache.handler(
                        "get tv by tmdb id",
                        page_key=tmdb_id,
                        function=tmdb.TV(tmdb_id).info,
                        cache_duration=GET_BY_TMDB_ID_CACHE_TIMEOUT,
                        kwargs={"append_to_response": extras},
                    ),
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
        return None

    def get_by_tvdb_id(self, tvdb_id):
        """Get a show or list of shows on TMDB through a TVDB ID.

        Args:
            id: An Integer or String containing the TVDB ID.
        """
        try:
            results = cache.handler(
                "get tv by tvdb id",
                page_key=tvdb_id,
                function=tmdb.Find(tvdb_id).info,
                cache_duration=GET_BY_TVDB_ID_CACHE_TIMEOUT,
                kwargs={"external_source": "tvdb_id"},
            )
            self._set_content_attributes("tv", results["tv_results"])
            return results
        except:
            log.handler(
                "Failed to obtain content with TVDB ID " + str(tvdb_id) + "!",
                log.ERROR,
                _logger,
            )
        return None

    # Cached or Threaded Functions
    def __all(self, page_number, page_multiplier):
        """Cacheable part of all()"""
        # Merge popular_movies, popular_tv, top_movies, and top_tv results together
        function_list = [
            self.popular_movies,
            self.popular_tv,
            self.top_movies,
            self.top_tv,
        ]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self._shuffle_results(self._merge_results(*results))

    def __tv(self, page_number, page_multiplier):
        """Cacheable part of tv()"""
        # Merge popular_tv and top_tv results together
        function_list = [self.popular_tv, self.top_tv]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self._shuffle_results(self._merge_results(*results))

    def __movies(self, page_number, page_multiplier):
        """Cacheable part of movies()"""
        # Merge popular_movies and top_movies results together
        function_list = [self.popular_movies, self.top_movies]
        results = threaded_execution(function_list, [page_number, page_multiplier])

        # Shuffle the results on each page
        return self._shuffle_results(self._merge_results(*results))

    def __recommended(self, tmdb_id, content_type, page_number):
        """Obtains recommendations given a TMDB ID.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
            page_number: An Integer that is the page number to return.
        """
        try:
            if content_type == "movie":
                return self._set_content_attributes(
                    content_type,
                    cache.handler(
                        "discover recommended movies",
                        page_key=str(tmdb_id) + "page" + str(page_number),
                        function=tmdb.Movies(tmdb_id).recommendations,
                        cache_duration=RECOMMENDED_CACHE_TIMEOUT,
                        kwargs={
                            "language": LANGUAGE,
                            "page": page_number,
                        },
                    ),
                )

            if content_type == "tv":
                return self._set_content_attributes(
                    content_type,
                    cache.handler(
                        "discover recommended tv",
                        page_key=str(tmdb_id) + "page" + str(page_number),
                        function=tmdb.TV(tmdb_id).recommendations,
                        cache_duration=RECOMMENDED_CACHE_TIMEOUT,
                        kwargs={
                            "language": LANGUAGE,
                            "page": page_number,
                        },
                    ),
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
        return None

    def __similar(self, tmdb_id, content_type, page_number):
        """Obtains similar content given a TMDB ID.

        Args:
            id: An Integer or String containing the TMDB ID.
            content_type: String containing "movie" or "tv".
            page_number: An Integer that is the page number to return.
        """
        try:
            if content_type == "movie":
                return self._set_content_attributes(
                    content_type,
                    cache.handler(
                        "discover similar movies",
                        page_key=str(tmdb_id) + "page" + str(page_number),
                        function=tmdb.Movies(tmdb_id).similar_movies,
                        cache_duration=SIMILAR_CACHE_TIMEOUT,
                        kwargs={
                            "language": LANGUAGE,
                            "page": page_number,
                        },
                    ),
                )

            if content_type == "tv":
                return self._set_content_attributes(
                    content_type,
                    cache.handler(
                        "discover similar tv",
                        page_key=str(tmdb_id) + "page" + str(page_number),
                        function=tmdb.TV(tmdb_id).similar,
                        cache_duration=SIMILAR_CACHE_TIMEOUT,
                        kwargs={
                            "language": LANGUAGE,
                            "page": page_number,
                        },
                    ),
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
        return None
