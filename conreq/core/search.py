"""Conreq Searching: Searches Sonarr and Radarr for content."""

from math import floor, log10
from threading import Thread

from conreq.core import cache, log
from conreq.core.generic_tools import clean_string
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
        log.configure(self.__logger, log.DEBUG)

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

            # Sort the results with our conreq ranking algorithm
            return self.__set_conreq_rank(query, results_list[0] + results_list[1])
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
            conreq_rank: Calculate conreq similarity ranking and sort the results (True/False)
        """
        try:
            return cache.handler(
                "sonarr search cache",
                self.__television,
                query,
                query=query,
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
            return cache.handler(
                "radarr search cache",
                self.__movie,
                query,
                query=query,
            )

        except:
            log.handler(
                "Searching for movie failed!",
                log.ERROR,
                self.__logger,
            )
            return []

    def __television(self, **kwargs):
        # Perform a search
        results = self.__sonarr.lookupSeries(kwargs["query"])

        # Set content type
        thread_list = []
        for result in results:
            thread = Thread(target=self.__set_content_type, args=[result, "tv"])
            thread.start()
            thread_list.append(thread)

        # Wait for computation to complete
        for thread in thread_list:
            thread.join()

        return self.__set_original_rank(results)

    def __movie(self, **kwargs):
        # Perform a search
        results = self.__radarr.lookupMovie(kwargs["query"])

        # Set content type
        thread_list = []
        for result in results:
            thread = Thread(target=self.__set_content_type, args=[result, "movie"])
            thread.start()
            thread_list.append(thread)

        # Wait for computation to complete
        for thread in thread_list:
            thread.join()

        return self.__set_original_rank(results)

    def __set_conreq_rank(self, query, results):
        # Determine string similarity and combined with a weight of the original rank
        clean_query = clean_string(query)
        thread_list = []
        for result in results:
            thread = Thread(
                target=self.__generate_conreq_rank, args=[result, clean_query]
            )
            thread.start()
            thread_list.append(thread)

        # Wait for computation to complete
        for thread in thread_list:
            thread.join()

        # Sort them by the new ranking metric
        return sorted(results, key=lambda i: i["conreqSimilarityRank"])

    def __set_original_rank(self, results):
        # Determine what search ranking was provided by Sonarr/Radarr
        try:
            thread_list = []
            for index, result in enumerate(results, start=1):
                thread = Thread(
                    target=self.__generate_original_rank, args=[result, index]
                )
                thread.start()
                thread_list.append(thread)

            # Wait for computation to complete
            for thread in thread_list:
                thread.join()

            # Sort them by the similarity metric
            return results
        except:
            log.handler("Failed to rank results", log.ERROR, self.__logger)
            return results

    def __generate_conreq_rank(self, result, clean_query):
        # Determines string similarity and combined with a weight of the original rank
        clean_title = clean_string(result["title"])

        # Multiplier if whole substring was found within the search result
        if clean_title.find(clean_query) != -1:
            query_substring_multiplier = 0.1
        else:
            query_substring_multiplier = 1

        # Generate similarity rank
        result["conreqSimilarityRank"] = (
            # Round the values to look pretty
            self.__round(
                # String similarity between the query and result
                (
                    self.__damerau.distance(clean_query, clean_title)
                    # Use sonarr/radarr's original rank as a weight/bias
                    * (result["arrOriginalRank"] / 10)
                )
                # Bias towards full substring matches
                * query_substring_multiplier
            )
            + 1
        )

    def __generate_original_rank(self, result, rank):
        # Sets the original rank based on the position Sonarr/Radarr
        result["arrOriginalRank"] = rank

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

    def __set_content_type(self, result, content_type):
        # Sets content type as "tv" or "movie"
        result["contentType"] = content_type


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
