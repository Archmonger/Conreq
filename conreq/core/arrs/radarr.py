"""Conreq Content Manager: Talks with Radarr in order to add/remove content."""

from pyarr import RadarrAPI

from conreq.core.server_settings.models import ConreqConfig
from conreq.utils import cache, log

from .base import ARR_LIBRARY_CACHE_TIMEOUT, ArrBase

_logger = log.get_logger(__name__)


class RadarrManager(ArrBase):
    """Adds and removes content from Radarr, and can return the request state."""

    def __init__(self) -> None:
        # Database values
        self.conreq_config = ConreqConfig.get_solo()

        # Connection to Radarr
        self.__radarr = RadarrAPI(
            self.conreq_config.radarr_url.rstrip("/"), self.conreq_config.radarr_api_key
        )

        # Set values if DB still contains default values
        self.check_radarr_defaults()

    def get(
        self,
        tmdb_id,
        force_update_cache=False,
    ) -> dict | None:
        """Gets content information and computes the availability of movies within the Radarr collection.

        Args:
            force_update_cache: Boolean. If True, arr library cache is force updated before returning results.
            tmdb_id: A string containing the TMDB ID.

        Returns:
            JSON response containing the existing content, filled with availability key-value pairs. \
            The availability has three available states: "Unavailable", "Partial", and "Available".
        """
        try:
            # Search for the TMDB ID within Radarr.
            # Get Radarr's collection
            results: dict = cache.handler(
                "radarr library",
                function=self.get_radarr_library,
                cache_duration=ARR_LIBRARY_CACHE_TIMEOUT,
                force_update_cache=force_update_cache,
            )
            assert isinstance(results, dict)

            # Find our TMDB ID within Radarr
            if str(tmdb_id) in results:
                return results[str(tmdb_id)]

            # Couldn't find the movie
            log.handler(
                f"Movie with TMDB ID {str(tmdb_id)} not found within Radarr.",
                log.INFO,
                _logger,
            )

        except KeyError:
            log.handler(
                "Content not ready yet!",
                log.WARNING,
                _logger,
            )

        except Exception:
            log.handler(
                "Failed to get content!",
                log.ERROR,
                _logger,
            )
        return None

    def add(
        self,
        tmdb_id,
        quality_profile_id,
        root_dir,
    ) -> dict | None:
        """Adds a new movie using Radarr.
        Will not work for content that already exists.
        This does NOT mark content as monitored or perform a search.

        Args:
            tmdb_id: A string containing the TMDB ID.
            quality_profile_id: An integer containing the quality profile ID (required).
            root_dir: A string containing the root directory (required).

        Returns:
            JSON response of adding the content.
        """
        try:
            # Add a movie with a specific TMDB ID to Radarr.
            movie = self.__radarr.lookup_movie(f"tmdb:{tmdb_id}")
            assert len(movie) == 1
            movie = movie[0]
            assert isinstance(movie, dict)

            response = self.__radarr.add_movie(
                movie=movie,
                root_dir=root_dir,
                quality_profile_id=quality_profile_id,
                search_for_movie=False,
                monitored=False,
                minimum_availability="released",
            )

            assert isinstance(response, dict)
            assert "title" in response
            return response

        except Exception:
            log.handler(
                "Failed to add content!",
                log.ERROR,
                _logger,
            )
        return None

    def request(
        self,
        radarr_id,
    ) -> dict | None:
        """Monitors and searches for an existing movie using Radarr.

        Args:
            radarr_id: An integer containing the Radarr ID.

        Returns:
            Dict containing movie_update_results and movie_search_results

        """
        try:
            # Search for a movie with a specific Radarr ID.
            response: dict = {
                "movie_update_results": [],
                "movie_search_results": [],
            }

            # Get the movie
            movie = self.__radarr.get_movie_by_movie_id(radarr_id)

            # Set the movie as monitored
            movie["monitored"] = True

            # Save the changes to Radarr
            response["movie_update_results"] = self.__radarr.upd_movie(
                movie, move_files=True
            )

            # Search for the movie
            response["movie_search_results"] = self.__radarr.post_command(
                name="MoviesSearch", movieIds=[radarr_id]
            )

            return response

        except Exception:
            log.handler(
                "Failed to request content!",
                log.ERROR,
                _logger,
            )
        return None

    def delete(
        self,
        radarr_id,
    ) -> dict | None:
        """Deletes an existing movie using Radarr.

        Args:
            radarr_id: An integer string containing the Radarr ID.

        Returns:
            JSON response of removing the content.
        """
        # TODO: Need to blacklist deleted content.
        try:
            # Remove a movie with a specific Radarr ID.
            return self.__radarr.del_movie(radarr_id, delete_files=True)

        except Exception:
            log.handler(
                "Failed to delete content!",
                log.ERROR,
                _logger,
            )
        return None

    def check_radarr_defaults(self) -> None:
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
                default_dirs = self.radarr_root_dirs()
                assert isinstance(default_dirs, list)
                default_dir = default_dirs[0]["id"]
                if not radarr_movies_folder:
                    self.conreq_config.radarr_movies_folder = default_dir
                if not radarr_anime_folder:
                    self.conreq_config.radarr_anime_folder = default_dir

            # Qualtiy Profiles
            if not radarr_movies_quality_profile or not radarr_anime_quality_profile:
                default_profiles = self.radarr_quality_profiles()
                assert isinstance(default_profiles, list)
                default_profile = default_profiles[0]["id"]
                if not radarr_movies_quality_profile:
                    self.conreq_config.radarr_movies_quality_profile = default_profile
                if not radarr_anime_quality_profile:
                    self.conreq_config.radarr_anime_quality_profile = default_profile

            # Save to DB
            if self.conreq_config.tracker.changed():
                self.conreq_config.clean_fields()
                self.conreq_config.save()

    def radarr_root_dirs(self) -> list | None:
        """Returns the root dirs available within Radarr"""
        try:
            return self.__radarr.get_root_folder()

        except Exception:
            log.handler(
                "Failed to get radarr root dirs!",
                log.ERROR,
                _logger,
            )
        return None

    def radarr_quality_profiles(self) -> list | None:
        """Returns the quality profiles available within Radarr"""
        try:
            return self.__radarr.get_quality_profile()

        except Exception:
            log.handler(
                "Failed to get radarr quality profiles!",
                log.ERROR,
                _logger,
            )
        return None

    def refresh_library(self) -> None:
        """Refreshes our local copy of Radarr's library"""
        try:
            if self.conreq_config.radarr_enabled:
                cache.handler(
                    "radarr library",
                    function=self.get_radarr_library,
                    cache_duration=ARR_LIBRARY_CACHE_TIMEOUT,
                    force_update_cache=True,
                )
        except Exception:
            log.handler(
                "Failed to refresh radarr!",
                log.WARNING,
                _logger,
            )

    def get_radarr_library(self) -> dict | None:
        """Fetches everything within Radarr's library"""
        try:
            if self.conreq_config.radarr_enabled:
                if self.conreq_config.radarr_url and self.conreq_config.radarr_api_key:
                    # Get the latest list of Radarr's collection
                    results = self.__radarr.get_movie()

                    # Set up a dictionary of results with IDs as keys
                    results_with_ids = {}
                    for movie in results:
                        if "tmdbId" in movie:
                            self._check_availability(movie)
                            self._set_content_attributes("movie", "radarr", movie)
                            results_with_ids[str(movie["tmdbId"])] = movie

                    # Return all movies
                    return results_with_ids

                log.handler(
                    "Radarr URL or API key is unset!",
                    log.WARNING,
                    _logger,
                )

        except Exception:
            log.handler(
                "Could not get movies!",
                log.ERROR,
                _logger,
            )
        return None
