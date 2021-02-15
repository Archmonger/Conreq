"""Conreq Content Manager: Talks with Sonarr/Radarr in order to add/remove content."""
from os.path import join as join_path

from conreq.apps.server_settings.models import ConreqConfig
from conreq.utils import cache, log
from PyArr import RadarrAPI, SonarrAPI

# Days, Hours, Minutes, Seconds
# Library is refreshed every minute as a background task
# This value is just a fail-safe.
ARR_LIBRARY_CACHE_TIMEOUT = 5 * 60


class ContentManager:
    """Adds and removes content from Sonarr and Radarr, and can return the request state."""

    def __init__(self):
        # Database values
        self.conreq_config = ConreqConfig.get_solo()

        # Connections to Sonarr and Radarr
        self.__sonarr = SonarrAPI(
            self.conreq_config.sonarr_url, self.conreq_config.sonarr_api_key
        )
        self.__radarr = RadarrAPI(
            self.conreq_config.radarr_url, self.conreq_config.radarr_api_key
        )

        # Creating a logger (for log files)
        self.__logger = log.get_logger(__name__)

    def get(self, obtain_season_info=False, force_update_cache=False, **kwargs):
        """Gets content information and computes the availability of movies, series, seasons, and episodes within the Sonarr or Radarr collection.

        Args:
            obtain_season_info: Boolean. If True, return season/episode information.
            force_update_cache: Boolean. If True, arr library cache is force updated before returning results.

            # Pick One ID
            tmdb_id: A string containing the TMDB ID.
            tvdb_id: A string containing the TVDB ID.

        Returns:
            1) JSON response containing the existing content, filled with availability key-value pairs.
               The availability has three available states: "Unavailable", "Partial", and "Available".
            2) None
        """
        try:
            # Search for the TMDB ID within Radarr.
            if kwargs.__contains__("tmdb_id"):
                # Get Radarr's collection
                results = cache.handler(
                    "radarr library",
                    function=self.get_radarr_library,
                    cache_duration=ARR_LIBRARY_CACHE_TIMEOUT,
                    force_update_cache=force_update_cache,
                )

                # Find our TMDB ID within Radarr
                if isinstance(results, dict) and results.__contains__(
                    str(kwargs["tmdb_id"])
                ):
                    return results[str(kwargs["tmdb_id"])]

                # Couldn't find the movie
                log.handler(
                    "Movie with TMDB ID "
                    + str(kwargs["tmdb_id"])
                    + " not found within Radarr.",
                    log.INFO,
                    self.__logger,
                )

            # Search for the TVDB ID within Sonarr.
            elif kwargs.__contains__("tvdb_id"):
                # Get Sonarr's collection
                results = cache.handler(
                    "sonarr library",
                    function=self.get_sonarr_library,
                    cache_duration=ARR_LIBRARY_CACHE_TIMEOUT,
                    force_update_cache=force_update_cache,
                )

                # Find our TVDB ID within Sonarr
                if isinstance(results, dict) and results.__contains__(
                    str(kwargs["tvdb_id"])
                ):
                    series = results[str(kwargs["tvdb_id"])]

                    # Obtain season information if needed
                    if obtain_season_info:
                        # Set the season and episode availability
                        self.__season_episode_availability(series)

                    return series

                # Couldn't find the series
                log.handler(
                    "Series with TVDB ID "
                    + str(kwargs["tvdb_id"])
                    + " not found within Sonarr.",
                    log.INFO,
                    self.__logger,
                )

            # Invalid parameter
            else:
                log.handler(
                    "A valid ID was not provided in ContentManager.get()!",
                    log.WARNING,
                    self.__logger,
                )

        except KeyError:
            log.handler(
                "Content not ready yet!",
                log.WARNING,
                self.__logger,
            )

        except:
            log.handler(
                "Failed to get content!",
                log.ERROR,
                self.__logger,
            )

    def add(self, **kwargs):
        """Adds a new movie or series using Sonarr or Radarr.
        Will not work for content that already exists.
        This does NOT mark content as monitored or perform a search.

        Args:
            quality_profile_id: An integer containing the quality profile ID (required).
            root_dir: A string containing the root directory (required).
            series_type: String containing Standard/Anime/Daily (required if adding TV).

            # Pick One ID
            tmdb_id: A string containing the TMDB ID.
            tvdb_id: A string containing the TVDB ID.

        Returns:
            1) JSON response of adding the content.
            2) None
        """
        try:
            # Add a movie with a specific TMDB ID to Radarr.
            if kwargs.__contains__("tmdb_id"):
                return self.__radarr.addMovie(
                    kwargs["tmdb_id"],
                    kwargs["quality_profile_id"],
                    join_path(kwargs["root_dir"], ""),
                    monitored=True,
                    searchForMovie=False,
                )

            # Add a show, season, or episode with a specific TVDB ID to Sonarr.
            elif kwargs.__contains__("tvdb_id"):
                # Add the show to Sonarr's collection
                series_id = self.__sonarr.addSeries(
                    kwargs["tvdb_id"],
                    kwargs["quality_profile_id"],
                    join_path(kwargs["root_dir"], ""),
                    seasonFolder=kwargs["season_folders"],
                    monitored=False,
                    ignoreEpisodesWithFiles=True,
                    ignoreEpisodesWithoutFiles=True,
                )["id"]

                # Obtain all information that Sonarr collected about the series
                new_series = self.__sonarr.getSeries(series_id)

                # Set the series type
                new_series["seriesType"] = kwargs["series_type"].lower().capitalize()
                return self.__sonarr.updSeries(new_series)

            # Invalid parameter
            else:
                log.handler(
                    "A valid ID was not provided in ContentManager.add()!",
                    log.WARNING,
                    self.__logger,
                )

        except:
            log.handler(
                "Failed to add content!",
                log.ERROR,
                self.__logger,
            )

    def request(self, **kwargs):
        """Monitors and searches for an existing movie, series, season(s), or episode(s) using Sonarr or Radarr.

        Args:
            # Pick One ID
            radarr_id: An integer containing the Radarr ID.
            sonarr_id: An integer containing the Sonarr ID.

            # Only used if using sonarr_id
            seasons: A list of integers containing the specific season numbers values (optional).
            episode_ids: A list of integers containing the specific "episodeId" values (optional).

        Returns:
            1) Dict containing
                "movie_update_results",
                "movie_search_results"
            2) Dict containing
                "season_update_results",
                "episode_update_results",
                "show_search_results",
                "season_search_results",
                "episode_search_results"
            3) None
        """
        try:
            # Search for a movie with a specific Radarr ID.
            if kwargs.__contains__("radarr_id"):
                response = {
                    "movie_update_results": None,
                    "movie_search_results": None,
                }

                # Get the movie
                movie = self.__radarr.getMovie(kwargs["radarr_id"])

                # Set the movie as monitored
                movie["monitored"] = True

                # Save the changes to Radarr
                response["movie_update_results"] = self.__radarr.updMovie(movie)

                movie_id = [
                    kwargs["radarr_id"],
                ]

                # Search for the movie
                response["movie_search_results"] = self.__radarr.setCommand(
                    name="MoviesSearch", movieIds=movie_id
                )

                return response

            # Search for a show with a specific Sonarr ID.
            elif kwargs.__contains__("sonarr_id"):
                response = {
                    "season_update_results": None,
                    "episode_update_results": None,
                    "show_search_results": None,
                    "season_search_results": None,
                    "episode_search_results": None,
                }

                # Get the series
                series = self.__sonarr.getSeries(kwargs["sonarr_id"])

                # Set the series as monitored
                series["monitored"] = True

                # Set specific seasons as monitored
                if kwargs.__contains__("seasons") and kwargs["seasons"] is not None:
                    for season in series["seasons"]:
                        if season["seasonNumber"] in kwargs["seasons"]:
                            season["monitored"] = True

                # Set every season as monitored if no seasons were specified
                else:
                    for season in series["seasons"]:
                        if season["seasonNumber"] != 0:
                            season["monitored"] = True

                # Save the changes to Sonarr
                response["season_update_results"] = self.__sonarr.updSeries(series)

                # Get the episodes
                episodes = self.__sonarr.getEpisodesBySeriesId(kwargs["sonarr_id"])
                modified_episodes = []
                response["episode_update_results"] = []

                # Set specific episodes as monitored
                if (
                    kwargs.__contains__("episode_ids")
                    and kwargs["episode_ids"] is not None
                ):
                    for episode in episodes:
                        if episode["id"] in kwargs["episode_ids"]:
                            episode["monitored"] = True
                            modified_episodes.append(episode)

                # Set every episode as monitored if no episodes were specified
                else:
                    for episode in episodes:
                        if episode["seasonNumber"] != 0:
                            episode["monitored"] = True
                            modified_episodes.append(episode)

                # Save the changes to Sonarr
                for episode in modified_episodes:
                    response["episode_update_results"].append(
                        self.__sonarr.updEpisode(episode)
                    )

                # Search for the whole show
                if (
                    not kwargs.__contains__("seasons") or kwargs["seasons"] is None
                ) and (
                    not kwargs.__contains__("episode_ids")
                    or kwargs["episode_ids"] is None
                ):
                    response["show_search_results"] = self.__sonarr.setCommand(
                        name="SeriesSearch", seriesId=kwargs["sonarr_id"]
                    )
                    return response

                # Search for specific seasons
                if kwargs.__contains__("seasons") and kwargs["seasons"] is not None:
                    response["season_search_results"] = []
                    for season in kwargs["seasons"]:
                        response["season_search_results"].append(
                            self.__sonarr.setCommand(
                                name="SeasonSearch",
                                seriesId=kwargs["sonarr_id"],
                                seasonNumber=season,
                            )
                        )

                # Search for specific episodes
                if (
                    kwargs.__contains__("episode_ids")
                    and kwargs["episode_ids"] is not None
                ):
                    response["episode_search_results"] = self.__sonarr.setCommand(
                        name="EpisodeSearch",
                        episodeIds=kwargs["episode_ids"],
                    )

                return response

            # Invalid parameter
            else:
                log.handler(
                    "A valid ID was not provided in ContentManager.request()!",
                    log.WARNING,
                    self.__logger,
                )

        except:
            log.handler(
                "Failed to request content!",
                log.ERROR,
                self.__logger,
            )

    def delete(self, **kwargs):
        """Deletes an existing movie, series, or episode(s) using Sonarr or Radarr.

        Kwargs:
            # Pick One ID
            radarr_id: An integer string containing the Radarr ID.
            sonarr_id: An integer containing the Sonarr ID.
            episode_file_ids: A list of integers containing the specific "episodeFileId" values.

        Returns:
            1) JSON response of removing the content.
            2) None
        """
        # TODO: Need to remove any currently downloading content for things that are removed.
        # TODO: Need to blacklist deleted content.
        try:
            # Remove a movie with a specific Radarr ID.
            if kwargs.__contains__("radarr_id"):
                return self.__radarr.delMovie(kwargs["radarr_id"], delFiles=True)

            # Remove a show with a specific Sonarr ID.
            elif kwargs.__contains__("sonarr_id"):
                # Remove the whole show
                return self.__sonarr.delSeries(kwargs["sonarr_id"], delFiles=True)

            # Remove episodes with Sonarr episode IDs.
            elif kwargs.__contains__("episode_file_ids"):
                response = []
                # Remove all episode files in the list
                for episode_id in kwargs["episode_file_ids"]:
                    response.append(
                        self.__sonarr.del_episode_file_by_episode_id(episode_id)
                    )

                return response

            # Invalid parameter
            else:
                log.handler(
                    "A valid ID was not provided in ContentManager.delete()!",
                    log.WARNING,
                    self.__logger,
                )

        except:
            log.handler(
                "Failed to delete content!",
                log.ERROR,
                self.__logger,
            )

    def redownload(self, **kwargs):
        """Deletes, requests, and adds an existing movie, series, or episode(s) using Sonarr or Radarr.

        Kwargs:
            # Pick One ID
            radarr_id: An integer containing the Radarr ID.
            sonarr_id: An integer containing the Sonarr ID.

            # Only used if using sonarr_id
            episode_file_ids: A list of integers containing the specific "episodeFileId" values (optional).
            seasons: A list of integers containing the specific season numbers values (optional).
            episode_ids: A list of integers containing the specific "episodeId" values (optional).

        Returns:
            1) Dict containing
                "movie_update_results",
                "movie_search_results"
            2) Dict containing
                "season_update_results",
                "episode_update_results",
                "show_search_results",
                "season_search_results",
                "episode_search_results"
            3) JSON response of removing the content.
            4) None
        """
        response = {}
        # Deletes the requested movie, series, seasons, or episodes
        response["delete_response"] = self.delete(**kwargs)
        # Requests the requested movie, series, seasons, or episodes
        response["request_response"] = self.request(**kwargs)

        # Return merged delete and request response
        return response

    def sonarr_root_dirs(self):
        """Returns the root dirs available within Sonarr"""
        try:
            return self.__sonarr.getRoot()

        except:
            log.handler(
                "Failed to get sonarr root dirs!",
                log.ERROR,
                self.__logger,
            )

    def radarr_root_dirs(self):
        """Returns the root dirs available within Radarr"""
        try:
            return self.__radarr.getRoot()

        except:
            log.handler(
                "Failed to get radarr root dirs!",
                log.ERROR,
                self.__logger,
            )

    def sonarr_quality_profiles(self):
        """Returns the quality profiles available within Sonarr"""
        try:
            return self.__sonarr.getQualityProfiles()

        except:
            log.handler(
                "Failed to get sonarr quality profiles!",
                log.ERROR,
                self.__logger,
            )

    def radarr_quality_profiles(self):
        """Returns the quality profiles available within Radarr"""
        try:
            return self.__radarr.getQualityProfiles()

        except:
            log.handler(
                "Failed to get radarr quality profiles!",
                log.ERROR,
                self.__logger,
            )

    def refresh_content(self):
        """Refreshes Sonarr and Radarr's content"""
        try:
            if self.conreq_config.radarr_enabled:
                cache.handler(
                    "radarr library",
                    function=self.get_radarr_library,
                    cache_duration=ARR_LIBRARY_CACHE_TIMEOUT,
                    force_update_cache=True,
                )
        except:
            log.handler(
                "Failed to refresh radarr!",
                log.WARNING,
                self.__logger,
            )

        try:
            if self.conreq_config.sonarr_enabled:
                cache.handler(
                    "sonarr library",
                    function=self.get_sonarr_library,
                    cache_duration=ARR_LIBRARY_CACHE_TIMEOUT,
                    force_update_cache=True,
                )
        except:
            log.handler(
                "Failed to refresh sonarr!",
                log.WARNING,
                self.__logger,
            )

    def get_radarr_library(self):
        """Fetches everything within Radarr's library"""
        try:
            if self.conreq_config.radarr_enabled:
                if self.conreq_config.radarr_url and self.conreq_config.radarr_api_key:
                    # Get the latest list of Radarr's collection
                    results = self.__radarr.getMovie()

                    # Set up a dictionary of results with IDs as keys
                    results_with_ids = {}
                    for movie in results:
                        if movie.__contains__("tmdbId"):
                            self.__check_availability(movie)
                            results_with_ids[str(movie["tmdbId"])] = movie

                    # Return all movies
                    return results_with_ids

                log.handler(
                    "Radarr URL or API key is unset!",
                    log.WARNING,
                    self.__logger,
                )

        except:
            log.handler(
                "Could not get movies!",
                log.ERROR,
                self.__logger,
            )

    def get_sonarr_library(self):
        """Fetches everything within Sonarr's library"""
        try:
            if self.conreq_config.sonarr_enabled:
                if self.conreq_config.sonarr_url and self.conreq_config.sonarr_api_key:
                    # Get the latest list of Sonarr's collection
                    results = self.__sonarr.getSeries()

                    # Set up a dictionary of results with IDs as keys
                    results_with_ids = {}
                    for series in results:
                        if series.__contains__("tvdbId"):
                            self.__check_availability(series)

                            results_with_ids[str(series["tvdbId"])] = series

                    # Return all movies
                    return results_with_ids

                log.handler(
                    "Sonarr URL or API key is unset!",
                    log.WARNING,
                    self.__logger,
                )

        except:
            log.handler(
                "Could not get series!",
                log.ERROR,
                self.__logger,
            )

    def __season_episode_availability(self, series):
        # Obtain the episodes
        episodes = self.__sonarr.getEpisodesBySeriesId(series["id"])
        for season in series["seasons"]:
            # Set the season availability
            self.__check_availability(season["statistics"])

            # Set the episode availability
            season["episodes"] = []
            for episode in episodes:
                if episode["seasonNumber"] == season["seasonNumber"]:
                    self.__check_availability(episode)
                    season["episodes"].append(episode)

    def __check_availability(self, content):

        #####################
        ### "Downloading" ###
        #####################
        # Use getQueue() to check if it's "downloading"
        # queue_data = self.__sonarr.getQueue()["status"]

        #####################
        ### "Unavailable" ###
        #####################
        # Check if an individual movie or episode does not exist (Sonarr and Radarr)
        try:
            if not content["hasFile"]:
                content["availability"] = "Unavailable"
                return content
        except:
            pass

        # Check if a season or series is completely unavailable (Sonarr)
        try:
            if content["episodeFileCount"] == 0:
                content["availability"] = "Unavailable"
                return content
        except:
            pass

        #################
        ### "Partial" ###
        #################
        # Check if season or series is partially downloaded (Sonarr)
        try:
            # Series
            if content.__contains__("lastInfoSync"):
                if (
                    content["episodeFileCount"] != 0
                    and content["episodeFileCount"] < content["episodeCount"]
                ):
                    content["availability"] = "Partial"
                    return content

            # Season
            elif (
                content["episodeFileCount"] != 0
                and content["totalEpisodeCount"] > content["episodeCount"]
            ):
                content["availability"] = "Partial"
                return content
        except:
            pass

        ###################
        ### "Available" ###
        ###################
        # Check if a season is fully downloaded (Sonarr)
        try:
            # Series
            if content.__contains__("lastInfoSync"):
                if (
                    content["episodeFileCount"] != 0
                    and content["episodeFileCount"] >= content["episodeCount"]
                ):
                    content["availability"] = "Available"
                    return content

            # Season
            elif (
                content["episodeFileCount"] != 0
                and content["totalEpisodeCount"] <= content["episodeCount"]
            ):
                content["availability"] = "Available"
                return content
        except:
            pass

        # Check if an individual movie or individual episode exists (Sonarr & Radarr)
        try:
            if content["hasFile"]:
                content["availability"] = "Available"
                return content
        except:
            pass

        log.handler(
            "Could not determine availability!\n" + str(content),
            log.INFO,
            self.__logger,
        )
        content["availability"] = "Unknown"
        return content
