from conreq.apps.user_requests.models import UserRequest
from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.utils import log
from conreq.utils.apps import set_many_availability
from conreq.utils.generic import is_key_value_in_list

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


def generate_requests_cards(user_requests):
    content_discovery = ContentDiscovery()
    content_manager = ContentManager()
    all_cards = []
    for entry in user_requests.values():
        # Fetch TMDB entry
        if entry["source"] == "tmdb":
            card = content_discovery.get_by_tmdb_id(
                tmdb_id=entry["content_id"],
                content_type=entry["content_type"],
                obtain_extras=False,
            )
            if card is not None:
                card["tmdbCard"] = True
                all_cards.append(card)

        # Fetch TVDB entry
        if entry["source"] == "tvdb":
            # Attempt to convert card to TMDB
            conversion = content_discovery.get_by_tvdb_id(tvdb_id=entry["content_id"])
            # Conversion found
            if conversion.__contains__("tv_results") and conversion["tv_results"]:
                card = conversion["tv_results"][0]
                card["tmdbCard"] = True
                all_cards.append(card)

                # Convert all requests to use this new ID
                old_requests = UserRequest.objects.filter(
                    content_id=entry["content_id"], source="tvdb"
                )
                old_requests.update(content_id=card["id"], source="tmdb")

            # Fallback to checking sonarr's database
            else:
                card = content_manager.get(tvdb_id=entry["content_id"])

                # Determine if the card has a known poster image
                if isinstance(card, dict):
                    card["contentType"] = entry["content_type"]
                    if card.__contains__("images"):
                        remote_poster = is_key_value_in_list(
                            "coverType", "poster", card["images"], return_item=True
                        )
                        if remote_poster:
                            card["remotePoster"] = remote_poster["remoteUrl"]

                all_cards.append(card)

        if card is None:
            log.handler(
                entry["content_type"]
                + " from "
                + entry["source"]
                + " with ID "
                + entry["content_id"]
                + " no longer exists!",
                log.WARNING,
                __logger,
            )

    # Set the availability
    content_discovery.determine_id_validity({"results": all_cards})
    set_many_availability(all_cards)

    return all_cards
