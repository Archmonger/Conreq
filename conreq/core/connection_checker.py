"""Conreq Connection Tester: Pings services to check availability."""
import re
from time import sleep

import requests
from conreq.utils import log

CONNECTION_RETRY_TIMEOUT = 1
MAX_CONNECTION_RETRIES = 5


class ConnectionChecker:
    """Checks the connection status to all of the available services"""

    # TODO: Add periodic pinging
    def __init__(
        self,
        tmdb_url,
        tmdb_api_key,
        sonarr_url,
        sonarr_api_key,
        radarr_url,
        radarr_api_key,
    ):

        # Default connection state
        self.tmdb_connection_status = False
        self.sonarr_connection_status = False
        self.radarr_connection_status = False

        # Initialized values
        # TODO: Obtain these values from the database on init
        self.__tmdb_url = tmdb_url
        self.__tmdb_endpoint = "/3/configuration?api_key="
        self.__tmdb_api_key = tmdb_api_key
        self.__sonarr_url = sonarr_url
        self.__sonarr_endpoint = "/api/system/status?apikey="
        self.__sonarr_api_key = sonarr_api_key
        self.__radarr_url = radarr_url
        self.__radarr_endpoint = "/api/system/status?apikey="
        self.__radarr_api_key = radarr_api_key

        # Creating a logger (for log files)
        self.__logger = log.get_logger(__name__)

        # Create some regex rules to validate links
        self.__url_validator = re.compile(
            r"^(?:http|ftp)s?://"  # protocol
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ip
            r"(?::\d+)?"  # port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

    def tmdb(self):
        """Returns True of a connection could be established to TMDB"""
        return self.__check_connection(
            self.__tmdb_url, self.__tmdb_endpoint, self.__tmdb_api_key
        )

    def sonarr(self):
        """Returns True of a connection could be established to Sonarr"""
        return self.__check_connection(
            self.__sonarr_url, self.__sonarr_endpoint, self.__sonarr_api_key
        )

    def radarr(self):
        """Returns True of a connection could be established to Radarr"""
        return self.__check_connection(
            self.__radarr_url, self.__radarr_endpoint, self.__radarr_api_key
        )

    def is_valid_url(self, url):
        """Checks if a string follows known URL patterns.

        Args:
            url: String containing a URL.
        """
        return re.match(self.__url_validator, url) is not None

    @staticmethod
    def __is_good_status(response_code):
        return bool(response_code in range(200, 299))

    def __check_connection(self, url, endpoint, key):
        connection_retries = 0
        connection_url = str(url) + str(endpoint) + str(key)

        if not self.is_valid_url(connection_url):
            log.handler(
                connection_url + " is likely an invalid URL. Trying anyways...",
                log.WARNING,
                self.__logger,
            )

        # Continue looping until a valid response code is detected
        while connection_retries < MAX_CONNECTION_RETRIES:
            try:
                # Try and get a response from the server
                response = requests.get(connection_url)
                response_code = response.status_code

                # If we got the response we're looking for, exit this loop
                if self.__is_good_status(response_code):
                    log.handler(
                        connection_url
                        + " pinged and a valid status code was returned.",
                        log.INFO,
                        self.__logger,
                    )
                    return True
            except:
                # If fetch resulted in an error, just continue the loop
                pass

            connection_retries = connection_retries + 1
            log.handler(
                "Failed communication with "
                + connection_url
                + ". Attempt "
                + str(connection_retries)
                + " of "
                + str(MAX_CONNECTION_RETRIES)
                + ".",
                log.WARNING,
                self.__logger,
            )

            # Wait a little bit before the next connection attempt
            sleep(CONNECTION_RETRY_TIMEOUT)

        return False


# Test driver code
if __name__ == "__main__":
    check = ConnectionChecker(
        "https://api.themoviedb.org",
        "x",
        "https://x",
        "x",
        "https://x",
        "x",
    )

    check.tmdb_connection_status = check.tmdb()
    check.sonarr_connection_status = check.sonarr()
    check.radarr_connection_status = check.radarr()

    print("TMDB: " + str(check.tmdb_connection_status))
    print("Sonarr: " + str(check.sonarr_connection_status))
    print("Radarr: " + str(check.radarr_connection_status))
