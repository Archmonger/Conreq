"""Conreq Content Manager: Talks with Sonarr in order to add/remove content."""
from conreq.core.server_settings.models import ConreqConfig
from conreq.utils import cache, log
from pyarr import SonarrAPI

from .base import ARR_LIBRARY_CACHE_TIMEOUT, ArrBase

_logger = log.get_logger(__name__)


class SonarrManager(ArrBase):
    """Adds and removes content from Sonarr, and can return the request state."""

    def __init__(self):
        # Database values
        self.conreq_config = ConreqConfig.get_solo()

        # Connections to Sonarr
        self.__sonarr = SonarrAPI(
            self.conreq_config.sonarr_url, self.conreq_config.sonarr_api_key
        )

        # Set values if DB still contains default values
        self.check_sonarr_defaults()

    def get(self, tvdb_id, obtain_season_info=False, force_update_cache=False):
        """Gets content information and computes the availability of series, seasons, and episodes within the Sonarr collection.

        Args:
            tvdb_id: A string containing the TVDB ID.
            obtain_season_info: Boolean. If True, return season/episode information.
            force_update_cache: Boolean. If True, arr library cache is force updated before returning results.

        Returns:
            JSON response containing the existing content, filled with availability key-value pairs.
               The availability has three available states: "Unavailable", "Partial", and "Available".
        """
        try:
            # Get Sonarr's collection
            results = cache.handler(
                "sonarr library",
                function=self.get_sonarr_library,
                cache_duration=ARR_LIBRARY_CACHE_TIMEOUT,
                force_update_cache=force_update_cache,
            )

            # Find our TVDB ID within Sonarr
            if isinstance(results, dict) and results.__contains__(str(tvdb_id)):
                series = results[str(tvdb_id)]

                # Obtain season information if needed
                if obtain_season_info:
                    # Set the season and episode availability
                    self._season_episode_availability(series)

                return series

            # Couldn't find the series
            log.handler(
                "Series with TVDB ID " + str(tvdb_id) + " not found within Sonarr.",
                log.INFO,
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

    def add(
        self, tvdb_id, quality_profile_id, root_dir, series_type, season_folders=True
    ):
        """Adds a new series using Sonarr.
        Will not work for content that already exists.
        This does NOT mark content as monitored or perform a search.

        Args:
            tvdb_id: A string containing the TVDB ID.
            quality_profile_id: An integer containing the quality profile ID (required).
            root_dir: A string containing the root directory (required).
            series_type: String containing Standard/Anime/Daily (required).
            season_folders: Boolean whether to use season folders

        Returns:
            JSON response of adding the content.
        """
        try:
            # Add the show to Sonarr's collection
            series_id = self.__sonarr.add_series(
                tvdb_id,
                quality_profile_id,
                root_dir,
                season_folder=season_folders,
                monitored=False,
                ignore_episodes_with_files=True,
                ignore_episodes_without_files=True,
            )["id"]

            # Obtain all information that Sonarr collected about the series
            new_series = self.__sonarr.get_series(series_id)

            # Set the series type
            new_series["seriesType"] = series_type.lower().capitalize()
            return self.__sonarr.upd_series(new_series)

        except:
            log.handler(
                "Failed to add content!",
                log.ERROR,
                _logger,
            )

    def request(self, sonarr_id, seasons=None, episode_ids=None):
        """Monitors and searches for an existing series, season(s), and/or episode(s) using Sonarr.

        Args:
            sonarr_id: An integer containing the Sonarr ID.
            seasons: A list of integers containing the specific season numbers values (optional).
            episode_ids: A list of integers containing the specific "episodeId" values (optional).

        Returns:
            Dict containing
                "season_update_results",
                "episode_update_results",
                "show_search_results",
                "season_search_results",
                "episode_search_results"
        """
        try:
            # Search for a show with a specific Sonarr ID.
            response = {
                "season_update_results": [],
                "episode_update_results": [],
                "show_search_results": [],
                "season_search_results": [],
                "episode_search_results": [],
            }

            # Get the series
            series = self.__sonarr.get_series(sonarr_id)

            # Set the series as monitored
            series["monitored"] = True

            # Set specific seasons as monitored
            if seasons:
                for season in series["seasons"]:
                    if season["seasonNumber"] in seasons:
                        season["monitored"] = True

            # Set every season as monitored if no seasons were specified
            else:
                for season in series["seasons"]:
                    if season["seasonNumber"] != 0:
                        season["monitored"] = True

            # Save the changes to Sonarr
            response["season_update_results"] = self.__sonarr.upd_series(series)

            # Get the episodes
            episodes = self.__sonarr.get_episodes_by_series_id(sonarr_id)
            modified_episodes = []
            response["episode_update_results"] = []

            # Set specific episodes as monitored
            if episode_ids:
                for episode in episodes:
                    if episode["id"] in episode_ids:
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
            if not seasons and not episode_ids:
                response["show_search_results"] = self.__sonarr.post_command(
                    name="SeriesSearch", seriesId=sonarr_id
                )
                return response

            # Search for specific seasons
            if seasons:
                response["season_search_results"] = []
                for season in seasons:
                    response["season_search_results"].append(
                        self.__sonarr.post_command(
                            name="SeasonSearch",
                            seriesId=sonarr_id,
                            seasonNumber=season,
                        )
                    )

            # Search for specific episodes
            if episode_ids:
                response["episode_search_results"] = self.__sonarr.post_command(
                    name="EpisodeSearch",
                    episodeIds=episode_ids,
                )

            return response

        except:
            log.handler(
                "Failed to request content!",
                log.ERROR,
                _logger,
            )

    def delete(self, sonarr_id):
        """Deletes an existing series using Sonarr.

        Args:
            sonarr_id: An integer containing the Sonarr show ID.

        Returns:
            JSON response of removing the content.
        """
        # TODO: Need to blacklist deleted content.
        try:
            # Remove a show with a specific Sonarr ID.
            return self.__sonarr.del_series(sonarr_id, delete_files=True)

        except:
            log.handler(
                "Failed to delete series!",
                log.ERROR,
                _logger,
            )

    def delete_episode(self, episode_file_id):
        """Deletes episode(s) using Sonarr.

        Args:
            episode_file_id: Integer containing the specific "episodeFileId" value.

        Returns:
            JSON response of removing the content.
        """
        # TODO: Need to blacklist deleted content.
        try:
            return self.__sonarr.del_episode_file(episode_file_id)

        except:
            log.handler(
                "Failed to delete episode!",
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

    def refresh_library(self):
        """Refreshes our local copy of Sonarr's library"""
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
                            self._check_availability(series)
                            self._set_content_attributes("tv", "sonarr", series)
                            results_with_ids[str(series["tvdbId"])] = series

                    # Return all series
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

    def _season_episode_availability(self, series):
        """Checks the availability of seasons."""
        # Obtain the episodes
        episodes = self.__sonarr.get_episodes_by_series_id(series["id"])
        for season in series["seasons"]:
            # Set the season availability
            self._check_availability(season["statistics"])

            # Set the episode availability
            season["episodes"] = []
            for episode in episodes:
                if episode["seasonNumber"] == season["seasonNumber"]:
                    self._check_availability(episode)
                    season["episodes"].append(episode)
