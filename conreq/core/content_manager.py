"""Conreq Content Manager: Talks with Sonarr/Radarr in order to add/remove content."""

from threading import Thread
from time import sleep

from conreq.core import cache, log
from conreq.core.thread_helper import ReturnThread
from PyArr import RadarrAPI, SonarrAPI


class ContentManager:
    """Adds and removes content from Sonarr and Radarr, and can return the request state.

    Args:
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

        # Creating a logger (for log files)
        self.__logger = log.get_logger("Content Discovery")
        log.configure(self.__logger, log.DEBUG)

        # Periodically run a task to re-populate the cache every minute
        Thread(target=self.refresh_content, daemon=True).start()

    def get(self, **kwargs):
        """Gets content information and computes the conreqStatus of movies, series, seasons, and episodes within the Sonarr or Radarr collection.

        Kwargs:
            tmdb_id: A string containing the TMDB ID.
            tvdb_id: An integer containing the TVDB ID.

        Returns:
            1) JSON response containing the existing content, filled with conreqStatus key-value pairs.
               conreqStatus has four available states: "Downloading", "Unavailable", "Partial", and "Available".
            2) None
        """
        try:
            # Search for the TMDB ID within Radarr.
            if kwargs.__contains__("tmdb_id"):
                # Get Radarr's collection
                results = cache.handler(
                    "radarr library cache",
                    self.__get_all_radarr_content,
                )

                # Find our TMDB ID within Radarr
                if results.__contains__(kwargs["tmdb_id"]):
                    return results[kwargs["tmdb_id"]]

                # Return None if couldn't find the movie
                log.handler(
                    "Movie with TMDB ID "
                    + str(kwargs["tmdb_id"])
                    + " not found within Radarr.",
                    log.INFO,
                    self.__logger,
                )
                return None

            # Search for the TVDB ID within Sonarr.
            if kwargs.__contains__("tvdb_id"):
                # Get Sonarr's collection

                results = cache.handler(
                    "sonarr library cache",
                    self.__get_all_sonarr_content,
                )

                # Find our TVDB ID within Sonarr
                if results.__contains__(kwargs["tvdb_id"]):
                    return results[kwargs["tvdb_id"]]

                # Return None if couldn't find the series
                log.handler(
                    "Series with TVDB ID "
                    + str(kwargs["tvdb_id"])
                    + " not found within Sonarr.",
                    log.INFO,
                    self.__logger,
                )
                return None

            # Invalid parameter
            log.handler(
                "Invalid parameter for getting content!",
                log.WARNING,
                self.__logger,
            )
            return None

        except:
            log.handler(
                "Failed to get content!",
                log.ERROR,
                self.__logger,
            )
            return None

    def add(self, **kwargs):
        """Adds a new movie or series using Sonarr or Radarr.
        Will not work for content that already exists.
        This does NOT mark content as monitored or perform a search.

        Kwargs:
            quality_profile_id: An integer containing the quality profile ID (required).
            root_dir: An string containing the root directory (required).

            # Pick One ID
            tmdb_id: A string containing the TMDB ID.
            tvdb_id: An integer containing the TVDB ID.

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
                    kwargs["root_dir"],
                    monitored=False,
                    searchForMovie=False,
                )

            # Add a show, season, or episode with a specific TVDB ID to Sonarr.
            if kwargs.__contains__("tvdb_id"):
                # Add the whole show to Sonarr's collection
                # Add the show to Sonarr's collection
                series_id = self.__sonarr.addSeries(
                    kwargs["tvdb_id"],
                    kwargs["quality_profile_id"],
                    kwargs["root_dir"],
                    monitored=False,
                    ignoreEpisodesWithFiles=True,
                    ignoreEpisodesWithoutFiles=True,
                )["id"]

                # Refresh Sonarr's information
                sleep(5)
                self.__sonarr.setCommand(name="RescanSeries", seriesId=series_id)
                self.__sonarr.setCommand(name="RefreshSeries", seriesId=series_id)

                # Obtain all information that Sonarr collected about the series
                new_series = self.__sonarr.getSeries(series_id)

                # Set the series type
                new_series["seriesType"] = kwargs["series_type"]
                return self.__sonarr.updSeries(new_series)

            # Invalid parameter
            log.handler(
                "Invalid parameter for adding content!",
                log.WARNING,
                self.__logger,
            )
            return None

        except:
            log.handler(
                "Failed to add content!",
                log.ERROR,
                self.__logger,
            )
            return None

    def request(self, **kwargs):
        """Monitors and searches for an existing movie, series, season(s), or episode(s) using Sonarr or Radarr.

        Kwargs:
            # Pick One ID
            radarr_id: A string containing the Radarr ID.
            sonarr_id: An integer containing the Sonarr ID.
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
            if kwargs.__contains__("sonarr_id"):
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
                if kwargs.__contains__("seasons"):
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
                if kwargs.__contains__("episode_ids"):
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
                if not kwargs.__contains__("seasons") and not kwargs.__contains__(
                    "episode_ids"
                ):
                    response["show_search_results"] = self.__sonarr.setCommand(
                        name="SeriesSearch", seriesId=kwargs["sonarr_id"]
                    )
                    return response

                # Search for specific seasons
                if kwargs.__contains__("seasons"):
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
                if kwargs.__contains__("episode_ids"):
                    response["episode_search_results"] = self.__sonarr.setCommand(
                        name="EpisodeSearch",
                        episodeIds=kwargs["episode_ids"],
                    )

                return response

            # Invalid parameter
            log.handler(
                "Invalid parameter for requesting content!",
                log.WARNING,
                self.__logger,
            )
            return None
        except:
            log.handler(
                "Failed to request content!",
                log.ERROR,
                self.__logger,
            )
            return None

    def delete(self, **kwargs):
        """Deletes an existing movie, series, or episode(s) using Sonarr or Radarr.

        Kwargs:
            # Pick One ID
            radarr_id: A string containing the Radarr ID.
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
            if kwargs.__contains__("sonarr_id"):
                # Remove the whole show
                return self.__sonarr.delSeries(kwargs["sonarr_id"], delFiles=True)

            # Remove episodes with Sonarr episode IDs.
            if kwargs.__contains__("episode_file_ids"):
                response = []
                # Remove all episode files in the list
                for episode_id in kwargs["episode_file_ids"]:
                    response.append(
                        self.__sonarr.del_episode_file_by_episode_id(episode_id)
                    )

                return response

            # Invalid parameter
            log.handler(
                "Invalid parameter for deleting content!",
                log.WARNING,
                self.__logger,
            )
            return None

        except:
            log.handler(
                "Failed to delete content!",
                log.ERROR,
                self.__logger,
            )
            return None

    def redownload(self, **kwargs):
        """Deletes, requests, and adds an existing movie, series, or episode(s) using Sonarr or Radarr.

        Kwargs:
            # Pick One ID
            radarr_id: A string containing the Radarr ID.
            sonarr_id: An integer containing the Sonarr ID.

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
        return self.__sonarr.getRoot()

    def radarr_root_dirs(self):
        """Returns the root dirs available within Radarr"""
        return self.__radarr.getRoot()

    def sonarr_quality_profiles(self):
        """Returns the quality profiles available within Sonarr"""
        return self.__sonarr.getQualityProfiles()

    def radarr_quality_profiles(self):
        """Returns the quality profiles available within Radarr"""
        return self.__radarr.getQualityProfiles()

    def check_download_status(self, **kwargs):
        """Check to see if Sonarr or Radarr content is being downloaded.
        Returns a list of everything being downloaded with a specific ID."""
        # TODO: Create this method and integrate into __check_status
        # Return a Percentage or None
        try:
            # Check download status for a specific movie in Radarr.
            if kwargs.__contains__("tmdb_id"):
                pass
            # Check download status for anything the related to a specific show in Sonarr.
            if kwargs.__contains__("tvdb_id"):
                pass
        except:
            pass

    def refresh_content(self):
        """Refreshes Sonarr and Radarr's content"""
        while 1:
            cache.handler(
                "radarr library cache",
                self.__get_all_radarr_content,
                cache_duration=None,
                force_update_cache=True,
            )

            cache.handler(
                "sonarr library cache",
                self.__get_all_sonarr_content,
                cache_duration=None,
                force_update_cache=True,
            )

            sleep(60)

    def __get_all_radarr_content(self):
        try:
            # Get the latest list of Radarr's collection
            results = self.__radarr.getMovie()

            # Set up a dictionary of results with IDs as keys
            results_with_ids = {}
            for movie in results:
                if movie.__contains__("tmdbId"):
                    self.__check_status(movie)
                    results_with_ids[movie["tmdbId"]] = movie

            # Return all movies
            return results_with_ids

        except:
            log.handler(
                "Could not get movies!",
                log.ERROR,
                self.__logger,
            )
            return None

    def __get_all_sonarr_content(self, get_seasons=False):
        try:
            # Get the latest list of Sonarr's collection
            results = self.__sonarr.getSeries()

            # Set up a dictionary of results with IDs as keys
            results_with_ids = {}
            for series in results:
                if series.__contains__("tvdbId"):
                    self.__check_status(series)

                    if get_seasons:
                        # Set the season and episode status codes
                        episodes = self.__sonarr.getEpisodesBySeriesId(series["id"])
                        self.__set_seasons_status(
                            seasons=series["seasons"],
                            episodes=episodes,
                        )

                    results_with_ids[series["tvdbId"]] = series

            # Return all movies
            return results_with_ids

        except:
            log.handler(
                "Could not get series!",
                log.ERROR,
                self.__logger,
            )
            return None

    def __set_seasons_status(self, **kwargs):
        # Set the season status codes
        season_threads = []
        episode_threads = []
        for season in kwargs["seasons"]:
            if not season.__contains__("statistics"):
                season["statistics"] = {}
                log.handler(
                    "Season did not contain any statistics!\n" + str(season),
                    log.WARNING,
                    self.__logger,
                )
            season_thread = Thread(
                target=self.__check_status, args=[season["statistics"]]
            )
            season_thread.start()
            season_threads.append(season_thread)

            # Set the episode status codes
            season["episodes"] = []
            for episode in kwargs["episodes"]:
                if episode["seasonNumber"] == season["seasonNumber"]:
                    episode_thread = ReturnThread(
                        target=self.__check_status, args=[episode]
                    )
                    episode_thread.start()
                    episode_threads.append(episode_thread)

            for thread in episode_threads:
                season["episodes"].append(thread.join())

        for thread in season_threads:
            thread.join()

        return kwargs["seasons"]

    def __check_status(self, content):

        ########################
        ### 0: "Downloading" ###
        ########################
        # Use getQueue() to get the "downloading" status code
        # queue_data = self.__sonarr.getQueue()["status"]

        ########################
        ### 1: "Unavailable" ###
        ########################
        # Check if an individual movie or episode does not exist (Sonarr and Radarr)
        try:
            if not content["hasFile"]:
                content["conreqStatus"] = "Unavailable"
                return content
        except:
            pass

        # Check if a season or series is completely unavailable (Sonarr)
        try:
            if content["episodeFileCount"] == 0:
                content["conreqStatus"] = "Unavailable"
                return content
        except:
            pass

        ####################
        ### 2: "Partial" ###
        ####################
        # Check if season or series is partially downloaded (Sonarr)
        try:
            # Series
            if content.__contains__("lastInfoSync"):
                if (
                    content["episodeFileCount"] != 0
                    and content["episodeFileCount"] < content["episodeCount"]
                ):
                    content["conreqStatus"] = "Partial"
                    return content

            # Season
            elif (
                content["episodeFileCount"] != 0
                and content["totalEpisodeCount"] > content["episodeCount"]
            ):
                content["conreqStatus"] = "Partial"
                return content
        except:
            pass

        ######################
        ### 3: "Available" ###
        ######################
        # Check if a season is fully downloaded (Sonarr)
        try:
            # Series
            if content.__contains__("lastInfoSync"):
                if (
                    content["episodeFileCount"] != 0
                    and content["episodeFileCount"] >= content["episodeCount"]
                ):
                    content["conreqStatus"] = "Available"
                    return content

            # Season
            elif (
                content["episodeFileCount"] != 0
                and content["totalEpisodeCount"] <= content["episodeCount"]
            ):
                content["conreqStatus"] = "Available"
                return content
        except:
            pass

        # Check if an individual movie or individual episode exists (Sonarr & Radarr)
        try:
            if content["hasFile"]:
                content["conreqStatus"] = "Available"
                return content
        except:
            pass

        log.handler(
            "Could not determine conreqStatus!\n" + str(content),
            log.WARNING,
            self.__logger,
        )
        content["conreqStatus"] = "Unknown"
        return content


if __name__ == "__main__":
    content_manager = ContentManager(
        "https://x",
        "x",
        "https://x",
        "x",
    )
    # print("\n#### Get Movies Test ####")
    # pprint(content_manager.get(tmdb_id="tt0114709"))
    # pprint(content_manager.get(tmdb_id="tt2245084"))

    # print("\n#### Get TV Test ####")
    # pprint(content_manager.get(tvdb_id=373345))
    # pprint(content_manager.get(tvdb_id=305074))

    # print("\n#### Sonarr Quality Profiles Test ####")
    # pprint(content_manager.sonarr_quality_profiles())
    # print("\n#### Radarr Quality Profiles Test ####")
    # pprint(content_manager.radarr_quality_profiles())

    # print("\n#### Sonarr Root Dirs Test ####")
    # pprint(content_manager.sonarr_root_dirs())
    # print("\n#### Radarr Root Dirs Test ####")
    # pprint(content_manager.radarr_root_dirs())

    # print("\n#### Add Movie Test ####")
    # radarr_root = content_manager.radarr_root_dirs()[0]["path"]
    # pprint(
    #     content_manager.add(
    #         tmdb_id="tt1979376", quality_profile_id=1, root_dir=radarr_root
    #     )
    # )

    # print("\n#### Add Anime Test ####")
    # sonarr_root = content_manager.sonarr_root_dirs()[0]["path"]
    # pprint(
    #     content_manager.add(
    #         tvdb_id="83277",
    #         series_type="Anime",
    #         quality_profile_id=1,
    #         root_dir=sonarr_root,
    #     )
    # )

    # print("\n#### Request TV Test ####")
    # pprint(content_manager.request(sonarr_id=30, episode_ids=[4635]))
    # pprint(content_manager.request(sonarr_id=30))
    # pprint(content_manager.request(sonarr_id=30, seasons=[1]))

    # print("\n#### Request Movies Test ####")
    # pprint(content_manager.request(radarr_id=4))

    # print("\n#### Redownload Movies Test")
    # pprint(content_manager.redownload(radarr_id=4))

    # print("\n#### Delete Test ####")
    # pprint(content_manager.delete(episode_file_ids=["210"]))
    # pprint(content_manager.delete(radarr_id=3))
