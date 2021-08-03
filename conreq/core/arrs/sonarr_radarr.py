"""Conreq Content Manager: Talks with Sonarr/Radarr in order to add/remove content."""
from os.path import join as join_path

from conreq.core.server_settings.models import ConreqConfig
from conreq.utils import cache, log
from pyarr import RadarrAPI, SonarrAPI

_logger = log.get_logger(__name__)

# Days, Hours, Minutes, Seconds
# Library is refreshed every minute as a background task
# This value is just a fail-safe.
ARR_LIBRARY_CACHE_TIMEOUT = 24 * 60 * 60


class ArrManager:
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

        # Set values if DB still contains default values
        self.check_sonarr_defaults()
        self.check_radarr_defaults()

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
                    _logger,
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
                    _logger,
                )

            # Invalid parameter
            else:
                log.handler(
                    "A valid ID was not provided in ContentManager.get()!",
                    log.WARNING,
                    _logger,
                )

        except KeyError:
            log.handler(
                "Content not ready yet!",
                log.WARNING,
                _logger,
            )

        except:
            log.handler(
                "Failed to get content!",
                log.ERROR,
                _logger,
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
                return self.__radarr.add_movie(
                    kwargs["tmdb_id"],
                    kwargs["quality_profile_id"],
                    join_path(kwargs["root_dir"], ""),
                    search_for_movie=False,
                )

            # Add a show, season, or episode with a specific TVDB ID to Sonarr.
            if kwargs.__contains__("tvdb_id"):
                # Add the show to Sonarr's collection
                series_id = self.__sonarr.add_series(
                    kwargs["tvdb_id"],
                    kwargs["quality_profile_id"],
                    join_path(kwargs["root_dir"], ""),
                    season_folder=kwargs["season_folders"],
                    monitored=False,
                    ignore_episodes_with_files=True,
                    ignore_episodes_without_files=True,
                )["id"]

                # Obtain all information that Sonarr collected about the series
                new_series = self.__sonarr.get_series(series_id)

                # Set the series type
                new_series["seriesType"] = kwargs["series_type"].lower().capitalize()
                return self.__sonarr.upd_series(new_series)

            # Invalid parameter
            log.handler(
                "A valid ID was not provided in ContentManager.add()!",
                log.WARNING,
                _logger,
            )

        except:
            log.handler(
                "Failed to add content!",
                log.ERROR,
                _logger,
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
            if kwargs.get("radarr_id"):
                response = {
                    "movie_update_results": [],
                    "movie_search_results": [],
                }

                # Get the movie
                movie = self.__radarr.get_movie(kwargs["radarr_id"])

                # Set the movie as monitored
                movie["monitored"] = True

                # Save the changes to Radarr
                response["movie_update_results"] = self.__radarr.upd_movie(
                    movie, move_files=True
                )

                movie_id = [
                    kwargs["radarr_id"],
                ]

                # Search for the movie
                response["movie_search_results"] = self.__radarr.post_command(
                    name="MoviesSearch", movieIds=movie_id
                )

                return response

            # Search for a show with a specific Sonarr ID.
            if kwargs.get("sonarr_id"):
                response = {
                    "season_update_results": [],
                    "episode_update_results": [],
                    "show_search_results": [],
                    "season_search_results": [],
                    "episode_search_results": [],
                }

                # Get the series
                series = self.__sonarr.get_series(kwargs["sonarr_id"])

                # Set the series as monitored
                series["monitored"] = True

                # Set specific seasons as monitored
                if kwargs.get("seasons"):
                    for season in series["seasons"]:
                        if season["seasonNumber"] in kwargs["seasons"]:
                            season["monitored"] = True

                # Set every season as monitored if no seasons were specified
                else:
                    for season in series["seasons"]:
                        if season["seasonNumber"] != 0:
                            season["monitored"] = True

                # Save the changes to Sonarr
                response["season_update_results"] = self.__sonarr.upd_series(series)

                # Get the episodes
                episodes = self.__sonarr.get_episodes_by_series_id(kwargs["sonarr_id"])
                modified_episodes = []
                response["episode_update_results"] = []

                # Set specific episodes as monitored
                if kwargs.get("episode_ids"):
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
                        self.__sonarr.upd_episode(episode)
                    )

                # Search for the whole show
                if not kwargs.get("seasons") and not kwargs.get("episode_ids"):
                    response["show_search_results"] = self.__sonarr.post_command(
                        name="SeriesSearch", seriesId=kwargs["sonarr_id"]
                    )
                    return response

                # Search for specific seasons
                if kwargs.get("seasons"):
                    response["season_search_results"] = []
                    for season in kwargs["seasons"]:
                        response["season_search_results"].append(
                            self.__sonarr.post_command(
                                name="SeasonSearch",
                                seriesId=kwargs["sonarr_id"],
                                seasonNumber=season,
                            )
                        )

                # Search for specific episodes
                if kwargs.get("episode_ids"):
                    response["episode_search_results"] = self.__sonarr.post_command(
                        name="EpisodeSearch",
                        episodeIds=kwargs["episode_ids"],
                    )

                return response

            # Invalid parameter
            log.handler(
                "A valid ID was not provided in ContentManager.request()!",
                log.WARNING,
                _logger,
            )

        except:
            log.handler(
                "Failed to request content!",
                log.ERROR,
                _logger,
            )

    def delete(self, **kwargs):
        """Deletes an existing movie, series, or episode(s) using Sonarr or Radarr.

        Kwargs:
            # Pick One ID
            radarr_id: An integer string containing the Radarr ID.
            sonarr_id: An integer containing the Sonarr ID.
            episode_file_id: Integers containing the specific "episodeFileId" value.

        Returns:
            1) JSON response of removing the content.
            2) None
        """
        # TODO: Need to blacklist deleted content.
        try:
            # Remove a movie with a specific Radarr ID.
            if kwargs.get("radarr_id"):
                return self.__radarr.del_movie(kwargs["radarr_id"], del_files=True)

            # Remove a show with a specific Sonarr ID.
            if kwargs.get("sonarr_id"):
                # Remove the whole show
                return self.__sonarr.del_series(kwargs["sonarr_id"], delete_files=True)

            # Remove episodes with Sonarr episode IDs.
            if kwargs.get("episode_file_id"):
                # Remove an episode file
                return self.__sonarr.del_episode_file(kwargs["episode_file_id"])

            # Invalid parameter
            log.handler(
                "A valid ID was not provided in ContentManager.delete()!",
                log.WARNING,
                _logger,
            )

        except:
            log.handler(
                "Failed to delete content!",
                log.ERROR,
                _logger,
            )

    def check_sonarr_defaults(self):
        """Will configure default root dirs and quality profiles (if unset)"""
        if self.conreq_config.sonarr_enabled:
            sonarr_tv_folder = self.conreq_config.sonarr_tv_folder
            sonarr_anime_folder = self.conreq_config.sonarr_anime_folder
            sonarr_tv_quality_profile = self.conreq_config.sonarr_tv_quality_profile
            sonarr_anime_quality_profile = (
                self.conreq_config.sonarr_anime_quality_profile
            )

            # Root dirs
            if not sonarr_tv_folder or not sonarr_anime_folder:
                default_dir = self.sonarr_root_dirs()[0]["id"]
                if not sonarr_tv_folder:
                    self.conreq_config.sonarr_tv_folder = default_dir
                if not sonarr_anime_folder:
                    self.conreq_config.sonarr_anime_folder = default_dir

            # Qualtiy Profiles
            if not sonarr_tv_quality_profile or not sonarr_anime_quality_profile:
                default_profile = self.sonarr_quality_profiles()[0]["id"]
                if not sonarr_tv_quality_profile:
                    self.conreq_config.sonarr_tv_quality_profile = default_profile
                if not sonarr_anime_quality_profile:
                    self.conreq_config.sonarr_anime_quality_profile = default_profile

            # Save to DB
            if self.conreq_config.tracker.changed():
                self.conreq_config.clean_fields()
                self.conreq_config.save()

    def check_radarr_defaults(self):
        """Will configure default root dirs and quality profiles (if unset)"""
        if self.conreq_config.radarr_enabled:
            radarr_movies_folder = self.conreq_config.radarr_movies_folder
            radarr_anime_folder = self.conreq_config.radarr_anime_folder
            radarr_movies_quality_profile = (
                self.conreq_config.radarr_movies_quality_profile
            )
            radarr_anime_quality_profile = (
                self.conreq_config.radarr_anime_quality_profile
            )

            # Root dirs
            if not radarr_movies_folder or not radarr_anime_folder:
                default_dir = self.radarr_root_dirs()[0]["id"]
                if not radarr_movies_folder:
                    self.conreq_config.radarr_movies_folder = default_dir
                if not radarr_anime_folder:
                    self.conreq_config.radarr_anime_folder = default_dir

            # Qualtiy Profiles
            if not radarr_movies_quality_profile or not radarr_anime_quality_profile:
                default_profile = self.radarr_quality_profiles()[0]["id"]
                if not radarr_movies_quality_profile:
                    self.conreq_config.radarr_movies_quality_profile = default_profile
                if not radarr_anime_quality_profile:
                    self.conreq_config.radarr_anime_quality_profile = default_profile

            # Save to DB
            if self.conreq_config.tracker.changed():
                self.conreq_config.clean_fields()
                self.conreq_config.save()

    def sonarr_root_dirs(self):
        """Returns the root dirs available within Sonarr"""
        try:
            return self.__sonarr.get_root_folder()

        except:
            log.handler(
                "Failed to get sonarr root dirs!",
                log.ERROR,
                _logger,
            )

    def radarr_root_dirs(self):
        """Returns the root dirs available within Radarr"""
        try:
            return self.__radarr.get_root_folder()

        except:
            log.handler(
                "Failed to get radarr root dirs!",
                log.ERROR,
                _logger,
            )

    def sonarr_quality_profiles(self):
        """Returns the quality profiles available within Sonarr"""
        try:
            return self.__sonarr.get_quality_profiles()

        except:
            log.handler(
                "Failed to get sonarr quality profiles!",
                log.ERROR,
                _logger,
            )

    def radarr_quality_profiles(self):
        """Returns the quality profiles available within Radarr"""
        try:
            return self.__radarr.get_quality_profiles()

        except:
            log.handler(
                "Failed to get radarr quality profiles!",
                log.ERROR,
                _logger,
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
                _logger,
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
                _logger,
            )

    def get_radarr_library(self):
        """Fetches everything within Radarr's library"""
        try:
            if self.conreq_config.radarr_enabled:
                if self.conreq_config.radarr_url and self.conreq_config.radarr_api_key:
                    # Get the latest list of Radarr's collection
                    results = self.__radarr.get_movie()

                    # Set up a dictionary of results with IDs as keys
                    results_with_ids = {}
                    for movie in results:
                        if movie.__contains__("tmdbId"):
                            self.__check_availability(movie)
                            self.__set_content_attributes("movie", "radarr", movie)
                            results_with_ids[str(movie["tmdbId"])] = movie

                    # Return all movies
                    return results_with_ids

                log.handler(
                    "Radarr URL or API key is unset!",
                    log.WARNING,
                    _logger,
                )

        except:
            log.handler(
                "Could not get movies!",
                log.ERROR,
                _logger,
            )

    def get_sonarr_library(self):
        """Fetches everything within Sonarr's library"""
        try:
            if self.conreq_config.sonarr_enabled:
                if self.conreq_config.sonarr_url and self.conreq_config.sonarr_api_key:
                    # Get the latest list of Sonarr's collection
                    results = self.__sonarr.get_series()

                    # Set up a dictionary of results with IDs as keys
                    results_with_ids = {}
                    for series in results:
                        if series.__contains__("tvdbId"):
                            self.__check_availability(series)
                            self.__set_content_attributes("tv", "sonarr", series)
                            results_with_ids[str(series["tvdbId"])] = series

                    # Return all movies
                    return results_with_ids

                log.handler(
                    "Sonarr URL or API key is unset!",
                    log.WARNING,
                    _logger,
                )

        except:
            log.handler(
                "Could not get series!",
                log.ERROR,
                _logger,
            )

    def __season_episode_availability(self, series):
        """Checks the availability of one item. For use within season_episode_availability()"""
        # Obtain the episodes
        episodes = self.__sonarr.get_episodes_by_series_id(series["id"])
        for season in series["seasons"]:
            # Set the season availability
            self.__check_availability(season["statistics"])

            # Set the episode availability
            season["episodes"] = []
            for episode in episodes:
                if episode["seasonNumber"] == season["seasonNumber"]:
                    self.__check_availability(episode)
                    season["episodes"].append(episode)

    @staticmethod
    def __set_content_attributes(content_type, content_source, results):
        """Sets the content type as tv/movie and content source as sonarr/radarr on a list of results"""
        try:
            # Set a list of results
            if isinstance(results, list):
                for result in results:
                    result["content_type"] = content_type
                    result["content_source"] = content_source
            # # Set a single media item
            else:
                results["content_type"] = content_type
                results["content_source"] = content_source
        except:
            log.handler(
                "Failed to set content attributes!",
                log.ERROR,
                _logger,
            )

    def __check_availability(self, content):
        """Checks the availability of one item. For use within check_availability()"""
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
            _logger,
        )
        content["availability"] = "Unknown"
        return content
