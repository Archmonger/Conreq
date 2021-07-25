"""Helpers for User Requests"""
from conreq.core.tmdb.discovery import TmdbDiscovery
from conreq.core.user_requests.models import UserRequest
from conreq.utils import log
from conreq.utils.multiprocessing import background_task, threaded_execution_unique_args
from conreq.utils.views import (
    add_unique_to_db,
    obtain_radarr_parameters,
    obtain_sonarr_parameters,
    set_many_availability,
)
from django.contrib.auth.models import AnonymousUser

_logger = log.get_logger(__name__)


def radarr_request_background_task(tmdb_id, content_manager, radarr_params, username):
    """Function that can be run in the background to request something on Radarr"""
    try:
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


def sonarr_request_background_task(
    tvdb_id, request_params, content_manager, sonarr_params, username
):
    """Function that can be run in the background to request something on Sonarr"""
    try:
        # Check if the show is already within Sonarr's collection
        show = content_manager.get(tvdb_id=tvdb_id)

        # If it doesn't already exists, add then request it
        if show is None:
            show = content_manager.add(
                tvdb_id=tvdb_id,
                quality_profile_id=sonarr_params["sonarr_profile_id"],
                root_dir=sonarr_params["sonarr_root"],
                series_type=sonarr_params["series_type"],
                season_folders=sonarr_params["season_folders"],
            )

        # Request
        content_manager.request(
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


def sonarr_request(
    tvdb_id, tmdb_id, request, request_params, content_manager, content_discovery
):
    """Request on Sonarr and save request history item to DB"""
    sonarr_params = obtain_sonarr_parameters(
        content_discovery, content_manager, tmdb_id, tvdb_id
    )

    # Request in the background
    background_task(
        sonarr_request_background_task,
        tvdb_id,
        request_params,
        content_manager,
        sonarr_params,
        request.user.username,
    )

    # Save to DB
    requested_by = request.user if not isinstance(request.user, AnonymousUser) else None
    add_unique_to_db(
        UserRequest,
        content_id=tmdb_id,
        content_type="tv",
        requested_by=requested_by,
    )


def radarr_request(tmdb_id, request, content_manager, content_discovery):
    """Request on Radarr and save request history item to DB"""
    radarr_params = obtain_radarr_parameters(
        content_discovery, content_manager, tmdb_id
    )

    # Request in the background
    background_task(
        radarr_request_background_task,
        tmdb_id,
        content_manager,
        radarr_params,
        request.user.username,
    )

    # Save to DB
    requested_by = request.user if not isinstance(request.user, AnonymousUser) else None
    add_unique_to_db(
        UserRequest,
        content_id=tmdb_id,
        content_type="movie",
        requested_by=requested_by,
    )


def __generate_request_card(entry, content_discovery):
    """Generates a single request card. This is intended for multi-threaded use."""
    card = None
    # Fetch TMDB entry
    card = content_discovery.get_by_tmdb_id(
        tmdb_id=entry["content_id"],
        content_type=entry["content_type"],
        obtain_extras=False,
    )
    card["requested_by"] = entry.get("requested_by__username")

    if card is None:
        log.handler(
            entry["content_type"]
            + " with ID "
            + entry["content_id"]
            + " no longer exists!",
            log.WARNING,
            _logger,
        )

    return card


def generate_requests_cards(user_requests):
    """Takes in a DB query containing requests, and pops out a list of their current request status"""
    content_discovery = TmdbDiscovery()
    all_cards = []
    function_list = []
    for request in user_requests:
        function_list.append(
            {
                "function": __generate_request_card,
                "args": [request, content_discovery],
            }
        )

    all_cards = threaded_execution_unique_args(function_list)
    content_discovery.determine_id_validity(all_cards)
    set_many_availability(all_cards)

    return all_cards
