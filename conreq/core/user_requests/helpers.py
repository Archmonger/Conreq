"""Helpers for User Requests"""
from django.contrib.auth.models import AnonymousUser

from conreq.core.discover.helpers import (
    obtain_radarr_parameters,
    obtain_sonarr_parameters,
    set_many_availability,
)
from conreq.core.tmdb.discovery import TmdbDiscovery
from conreq.core.user_requests.models import UserRequest
from conreq.utils import log
from conreq.utils.database import add_unique_to_db
from conreq.utils.threads import threaded_execution_unique_args

from .tasks import radarr_request_background_task, sonarr_request_background_task

_logger = log.get_logger(__name__)


def sonarr_request(tvdb_id, tmdb_id, request, request_params):
    """Request on Sonarr and save request history item to DB"""
    sonarr_params = obtain_sonarr_parameters(tmdb_id, tvdb_id)

    # Request in the background
    sonarr_request_background_task(
        tvdb_id,
        request_params,
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


def radarr_request(tmdb_id, request):
    """Request on Radarr and save request history item to DB"""
    radarr_params = obtain_radarr_parameters(tmdb_id)

    # Request in the background
    radarr_request_background_task(
        tmdb_id,
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
