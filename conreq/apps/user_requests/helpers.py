"""Helpers for User Requests"""
from conreq.apps.base.tasks import background_task
from conreq.apps.user_requests.models import UserRequest
from conreq.core.tmdb.discovery import TmdbDiscovery
from conreq.core.content_manager import ContentManager
from conreq.utils import log
from conreq.utils.views import (
    add_unique_to_db,
    obtain_radarr_parameters,
    obtain_sonarr_parameters,
    set_many_availability,
)
from conreq.utils.generic import is_key_value_in_list
from conreq.utils.multiprocessing import threaded_execution_unique_args

_logger = log.get_logger(__name__)


def radarr_request_background_task(tmdb_id, content_manager, radarr_params, username):
    """Function that can be run in the background to request something on Radarr"""
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
        _logger,
    )


def sonarr_request_background_task(
    tvdb_id, request_parameters, content_manager, sonarr_params, username
):
    """Function that can be run in the background to request something on Sonarr"""
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
        seasons=request_parameters["seasons"],
        episode_ids=request_parameters["episode_ids"],
    )

    log.handler(
        username + " requested TV series " + show["title"],
        log.INFO,
        _logger,
    )


def sonarr_request(
    tvdb_id, tmdb_id, request, request_parameters, content_manager, content_discovery
):
    """Request on Sonarr and save request history item to DB"""
    sonarr_params = obtain_sonarr_parameters(
        content_discovery, content_manager, tmdb_id, tvdb_id
    )

    # Request in the background
    background_task(
        sonarr_request_background_task,
        tvdb_id,
        request_parameters,
        content_manager,
        sonarr_params,
        request.user.username,
    )

    # Save to DB
    if tmdb_id:
        content_id = tmdb_id
        source = "tmdb"
    else:
        content_id = tvdb_id
        source = "tvdb"
    add_unique_to_db(
        UserRequest,
        content_id=content_id,
        source=source,
        content_type="tv",
        requested_by=request.user,
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
    add_unique_to_db(
        UserRequest,
        content_id=tmdb_id,
        source="tmdb",
        content_type="movie",
        requested_by=request.user,
    )


def __generate_request_card(entry, content_discovery, content_manager):
    """Generates a single request card. This is intended for multi-threaded use."""
    card = None
    # Fetch TMDB entry
    if entry["source"] == "tmdb":
        card = content_discovery.get_by_tmdb_id(
            tmdb_id=entry["content_id"],
            content_type=entry["content_type"],
            obtain_extras=False,
        )
        card["requested_by"] = entry.get("requested_by__username")

    # Fetch TVDB entry
    elif entry["source"] == "tvdb":
        # Attempt to convert card to TMDB
        conversion = content_discovery.get_by_tvdb_id(tvdb_id=entry["content_id"])
        # Conversion found
        if conversion.__contains__("tv_results") and conversion["tv_results"]:
            card = conversion["tv_results"][0]
            card["requested_by"] = entry.get("requested_by__username")

            # Convert all requests to use this new ID
            old_requests = UserRequest.objects.filter(
                content_id=entry["content_id"], source="tvdb"
            )
            old_requests.update(content_id=card["id"], source="tmdb")

        # Fallback to checking sonarr's database
        else:
            card = content_manager.get(tvdb_id=entry["content_id"])
            card["requested_by"] = entry.get("requested_by__username")

            # Determine if the card has a known poster image
            if isinstance(card, dict):
                card["content_type"] = entry["content_type"]
                if card.__contains__("images"):
                    remote_poster = is_key_value_in_list(
                        "coverType", "poster", card["images"], return_item=True
                    )
                    if remote_poster:
                        card["remotePoster"] = remote_poster["remoteUrl"]

    if card is None:
        log.handler(
            entry["content_type"]
            + " from "
            + entry["source"]
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
    content_manager = ContentManager()
    all_cards = []
    function_list = []
    for request in user_requests:
        function_list.append(
            {
                "function": __generate_request_card,
                "args": [request, content_discovery, content_manager],
            }
        )

    all_cards = threaded_execution_unique_args(function_list)
    content_discovery.determine_id_validity(all_cards)
    set_many_availability(all_cards)

    return all_cards
