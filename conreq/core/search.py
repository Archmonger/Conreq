"""Conreq Searching: Searches Sonarr and Radarr for content."""

from math import floor, log10
from re import sub as substitution

from conreq.core import cache, log
from conreq.core.thread_helper import ReturnThread
from PyArr import RadarrAPI, SonarrAPI
from similarity.damerau import Damerau


class Search:
    """Searches Sonarr and Radarr for a given query
    >>> Args:
        sonarr_url: String containing the Sonarr URL.
        sonarr_api_key: String containing the Sonarr API key.
        radarr_url: String containing the Radarr URL.
        radarr_api_key: String containing the Radarr API key.
    """

    def __init__(
        self,
        sonarr_url,
        sonarr_api_key,
        radarr_url,
        radarr_api_key,
    ):
        # Initialized values
        # TODO: Obtain these values from the database on init
        self.__sonarr_url = sonarr_url
        self.__sonarr_api_key = sonarr_api_key
        self.__radarr_url = radarr_url
        self.__radarr_api_key = radarr_api_key

        # Connections to Sonarr and Radarr
        self.__sonarr = SonarrAPI(self.__sonarr_url, self.__sonarr_api_key)
        self.__radarr = RadarrAPI(self.__radarr_url, self.__radarr_api_key)

        # Algorithm for determining string similarity
        self.__damerau = Damerau()

        # Create a logger (for log files)
        self.__logger = log.get_logger("Search")
        log.configure(self.__logger, log.WARNING)

        # Set up result caching dictionaries
        # key = query, value = page contents
        self.__movie_cache = {}
        self.__television_cache = {}
        # key = query, value = time when cached
        self.__movie_cache_time = {}
        self.__television_cache_time = {}

    def all(self, query):
        """Search Sonarr and Radarr for a query. Sort the
        results based on their similiarity to the query.

        Args:
            query: A string containing a search term.
        """
        try:
            thread_list = []

            # Start query for TV
            thread = ReturnThread(target=self.television, args=[query])
            thread.start()
            thread_list.append(thread)

            # Start query for movie
            thread = ReturnThread(target=self.movie, args=[query])
            thread.start()
            thread_list.append(thread)

            # Wait for query completion
            results_list = []
            for thread in thread_list:
                results_list.append(thread.join())

            return self.__sort_ranked_results(query, results_list[0] + results_list[1])
        except:
            log.handler(
                "Searching for all failed!",
                log.ERROR,
                self.__logger,
            )
            return []

    def television(self, query):
        """Search Sonarr for a query.

        Args:
            query: A string containing a search term.
        """
        try:
            return self.__rank_results(
                cache.handler(
                    self.__television_cache,
                    self.__television_cache_time,
                    self.__television,
                    query,
                    query=query,
                )
            )

        except:
            log.handler(
                "Searching for TV failed!",
                log.ERROR,
                self.__logger,
            )
            return []

    def movie(self, query):
        """Search Radarr for a query.

        Args:
            query: A string containing a search term.
        """
        try:
            return self.__rank_results(
                cache.handler(
                    self.__movie_cache,
                    self.__movie_cache_time,
                    self.__movie,
                    query,
                    query=query,
                )
            )
        except:
            log.handler(
                "Searching for movie failed!",
                log.ERROR,
                self.__logger,
            )
            return []

    def __television(self, **kwargs):
        if kwargs.__contains__("query"):
            # Perform a search and set the conreqSource
            results = self.__sonarr.lookupSeries(kwargs["query"])
            for result in results:
                result["conreqSource"] = "sonarr"
            return results

        # Required kwargs was not found
        raise KeyError

    def __movie(self, **kwargs):
        if kwargs.__contains__("query"):
            # Perform a search and set the conreqSource
            results = self.__radarr.lookupMovie(kwargs["query"])
            for result in results:
                result["conreqSource"] = "radarr"
            return results

        # Required kwargs was not found
        raise KeyError

    def __sort_ranked_results(self, query, results):
        # Determine string similarity and combined with a weight of the original rank
        clean_query = self.__clean_str(query)
        for result in results:
            result["conreqNewRank"] = (
                # Round the values to look pretty
                self.__round(
                    # String similarity between the query and result
                    self.__damerau.distance(
                        clean_query, self.__clean_str(result["title"])
                    )
                    # Use sonarr/radarr's original rank as a weight/bias
                    * (result["conreqOriginalRank"] / 10)
                )
                + 1
            )
        # Sort them by the new ranking metric
        return sorted(results, key=lambda i: i["conreqNewRank"])

    def __rank_results(self, results):
        # Calculate a value to determine string similarity
        try:
            count = 1
            for result in results:
                result["conreqOriginalRank"] = count
                count = count + 1
            # Sort them by the similarity metric
            return results
        except:
            log.handler("Failed to rank results", log.ERROR, self.__logger)
            return results

    def __clean_str(self, string):
        # Removes non-alphanumerics from a string
        try:
            return substitution(r"\W+", "", string)
        except:
            log.handler(
                "Cleaning the string failed!",
                log.ERROR,
                self.__logger,
            )
            return ""

    def __round(self, number, significant_figures=5):
        # Round a number using the concept of significant figures
        try:
            # Rounding would've returned an error if the number is 0
            if number == 0:
                return number

            # Round a non-zero number
            return round(number, -int(floor(log10(number))) + (significant_figures - 1))
        except:
            log.handler("Failed to round!", log.ERROR, self.__logger)
            return number


# Test driver code
if __name__ == "__main__":
    search = Search(
        "x",
        "x",
        "x",
        "x",
    )

    # print("\n#### Find Movies Test ####")
    # pprint(search.movie("Finding Nemo")[:5])
    # print("\n#### Find TV Test ####")
    # pprint(search.television("Toradora")[:5])
    # print("\n#### Find All Test ####")
    # pprint(search.all("The Black")[:5])
    # print("\n#### Find All Test (Cached) ####")
    # pprint(search.all("The Black")[:5])
