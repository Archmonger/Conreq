from conreq.core.arrs.radarr import RadarrManager
from conreq.core.arrs.sonarr import SonarrManager
from conreq.utils import log
from huey.contrib.djhuey import db_task

_logger = log.get_logger(__name__)


@db_task()
def sonarr_request_background_task(tvdb_id, request_params, sonarr_params, username):
    """Function that can be run in the background to request something on Sonarr"""
    try:
        sonarr_manager = SonarrManager()
        # Check if the show is already within Sonarr's collection
        show = sonarr_manager.get(tvdb_id=tvdb_id)

        # If it doesn't already exists, add then request it
        if show is None:
            show = sonarr_manager.add(
                tvdb_id=tvdb_id,
                quality_profile_id=sonarr_params["sonarr_profile_id"],
                root_dir=sonarr_params["sonarr_root"],
                series_type=sonarr_params["series_type"],
                season_folders=sonarr_params["season_folders"],
            )

        # Request
        sonarr_manager.request(
            sonarr_id=show["id"],
            seasons=request_params.get("seasons"),
            episode_ids=request_params.get("episode_ids"),
        )

        username = username if username else "API"
        log.handler(
            username + " requested TV series " + show["title"],
            log.INFO,
            _logger,
        )
    except:
        if "show" not in locals():
            show = {"title": "Conreq Uninitialized"}
        log.handler(
            "\n".join(
                (
                    "Failed to request on Radarr!",
                    f"tvdb_id: {tvdb_id}",
                    f"request_params: {request_params}",
                    f"sonarr_params: {sonarr_params}",
                    f"show: {show}",
                    f"username: {username}",
                )
            ),
            log.ERROR,
            _logger,
        )


@db_task()
def radarr_request_background_task(tmdb_id, radarr_params, username):
    """Function that can be run in the background to request something on Radarr"""
    try:
        radarr_manager = RadarrManager()
        # Check if the movie is already within Radarr's collection
        movie = radarr_manager.get(tmdb_id=tmdb_id)

        # If it doesn't already exists, add then request it
        if movie is None:
            movie = radarr_manager.add(
                tmdb_id=tmdb_id,
                quality_profile_id=radarr_params["radarr_profile_id"],
                root_dir=radarr_params["radarr_root"],
            )

        # Request
        radarr_manager.request(radarr_id=movie["id"])

        username = username if username else "API"
        log.handler(
            username + " requested movie " + movie["title"],
            log.INFO,
            _logger,
        )
    except:
        if "movie" not in locals():
            movie = {"title": "Conreq Uninitialized"}
        log.handler(
            "\n".join(
                (
                    "Failed to request on Radarr!",
                    f"tmdb_id: {tmdb_id}",
                    f"radarr_params: {radarr_params}",
                    f"movie: {movie}",
                    f"username: {username}",
                )
            ),
            log.ERROR,
            _logger,
        )
