import json

from conreq.apps.user_requests.models import UserRequest
from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.utils import log
from conreq.utils.apps import (
    add_request_to_db,
    generate_context,
    obtain_radarr_parameters,
    obtain_sonarr_parameters,
    request_is_unique,
    set_many_conreq_status,
)
from conreq.utils.generic import is_key_value_in_list
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page

# Days, Hours, Minutes, Seconds
INVITE_CODE_DURATION = 7 * 24 * 60 * 60
__logger = log.get_logger(__name__)

# Create your views here.
@login_required
def request_content(request):
    # User submitted a new request
    if request.method == "POST":
        request_parameters = json.loads(request.body.decode("utf-8"))
        log.handler(
            "Request received: " + str(request_parameters),
            log.INFO,
            __logger,
        )

        content_manager = ContentManager()
        content_discovery = ContentDiscovery()

        # TV show was requested
        if request_parameters["content_type"] == "tv":
            # Obtain the TVDB ID if needed
            tvdb_id = request_parameters["tvdb_id"]
            tmdb_id = request_parameters["tmdb_id"]
            if tvdb_id is None and tmdb_id is not None:
                tvdb_id = content_discovery.get_external_ids(tmdb_id, "tv")["tvdb_id"]

            # Request the show by the TVDB ID
            if tvdb_id is not None:
                # Check if the show is already within Sonarr's collection
                show = content_manager.get(tvdb_id=tvdb_id)

                # If it doesn't already exists, add then request it
                if show is None:
                    sonarr_params = obtain_sonarr_parameters(
                        content_discovery, content_manager, tmdb_id, tvdb_id
                    )
                    show = content_manager.add(
                        tvdb_id=tvdb_id,
                        quality_profile_id=sonarr_params["sonarr_profile_id"],
                        root_dir=sonarr_params["sonarr_root"],
                        series_type=sonarr_params["series_type"],
                        season_folders=sonarr_params["season_folders"],
                    )

                # Save and request
                if tmdb_id:
                    add_request_to_db(
                        content_id=tmdb_id,
                        source="tmdb",
                        content_type="tv",
                        user=request.user,
                    )
                else:
                    add_request_to_db(
                        content_id=tvdb_id,
                        source="tvdb",
                        content_type="tv",
                        user=request.user,
                    )
                content_manager.request(
                    sonarr_id=show["id"],
                    seasons=request_parameters["seasons"],
                    episode_ids=request_parameters["episode_ids"],
                )

                log.handler(
                    request.user.username + " requested TV series " + show["title"],
                    log.INFO,
                    __logger,
                )

        # Movie was requested
        elif request_parameters["content_type"] == "movie":
            tmdb_id = request_parameters["tmdb_id"]
            radarr_params = obtain_radarr_parameters(
                content_discovery, content_manager, tmdb_id
            )

            # Check if the movie is already within Radarr's collection
            movie = content_manager.get(tmdb_id=tmdb_id)

            # If it doesn't already exists, add then request it
            if movie is None:
                movie = content_manager.add(
                    tmdb_id=tmdb_id,
                    quality_profile_id=radarr_params["radarr_profile_id"],
                    root_dir=radarr_params["radarr_root"],
                )

            # Save and request
            add_request_to_db(
                content_id=tmdb_id,
                source="tmdb",
                content_type="movie",
                user=request.user,
            )
            content_manager.request(radarr_id=movie["id"])

            log.handler(
                request.user.username + " requested movie " + movie["title"],
                log.INFO,
                __logger,
            )

        return JsonResponse({})

    return HttpResponseForbidden()


@cache_page(1)
@login_required
def my_requests(request):
    template = loader.get_template("viewport/requests.html")

    content_discovery = ContentDiscovery()
    content_manager = ContentManager()
    user_requests = (
        UserRequest.objects.filter(requested_by=request.user).order_by("id").reverse()
    )

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
                    content_id=entry["content_id"]
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
    set_many_conreq_status(all_cards)

    context = generate_context({"all_cards": all_cards})

    return HttpResponse(template.render(context, request))


@cache_page(1)
@login_required
def all_requests(request):
    template = loader.get_template("viewport/requests.html")

    content_discovery = ContentDiscovery()
    content_manager = ContentManager()
    user_requests = UserRequest.objects.all().order_by("id").reverse()

    all_cards = []
    request_dict = {}

    for entry in user_requests.values():
        # Fetch TMDB entry
        if entry["source"] == "tmdb" and request_is_unique(entry, request_dict):
            card = content_discovery.get_by_tmdb_id(
                tmdb_id=entry["content_id"],
                content_type=entry["content_type"],
                obtain_extras=False,
            )
            if card is not None:
                card["tmdbCard"] = True
                all_cards.append(card)

        # Fetch TVDB entry
        if entry["source"] == "tvdb" and request_is_unique(entry, request_dict):
            # Attempt to convert card to TMDB
            conversion = content_discovery.get_by_tvdb_id(tvdb_id=entry["content_id"])
            # Conversion found
            if conversion.__contains__("tv_results") and conversion["tv_results"]:
                card = conversion["tv_results"][0]
                card["tmdbCard"] = True
                all_cards.append(card)

                # Convert all requests to use this new ID
                old_requests = UserRequest.objects.filter(
                    content_id=entry["content_id"]
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

        if card is None and not request_is_unique(entry, request_dict):
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
    set_many_conreq_status(all_cards)

    context = generate_context({"all_cards": all_cards})

    return HttpResponse(template.render(context, request))
