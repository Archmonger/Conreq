from conreq.utils import log

__logger = log.get_logger(__name__)


def add_save_request_movie(content_manager, tmdb_id, radarr_params, username):
    # Check if the movie is already within Radarr's collection
    movie = content_manager.get(tmdb_id=tmdb_id)

    # If it doesn't already exists, add then request it
    if movie is None:
        movie = content_manager.add(
            tmdb_id=tmdb_id,
            quality_profile_id=radarr_params["radarr_profile_id"],
            root_dir=radarr_params["radarr_root"],
        )

    # Request
    content_manager.request(radarr_id=movie["id"])

    log.handler(
        username + " requested movie " + movie["title"],
        log.INFO,
        __logger,
    )
