import json

from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.utils import log
from conreq.utils.apps import (
    add_request_to_db,
    obtain_radarr_parameters,
    obtain_sonarr_parameters,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse

# Days, Hours, Minutes, Seconds
INVITE_CODE_DURATION = 7 * 24 * 60 * 60
__logger = log.get_logger(__name__)

# Create your views here.
@login_required
def request_content(request):
    # User submitted the registration form
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
                preexisting_show = content_manager.get(tvdb_id=tvdb_id)

                # If it doesn't already exists, add then request it
                if preexisting_show is None:
                    sonarr_params = obtain_sonarr_parameters(
                        content_discovery, content_manager, tmdb_id, tvdb_id
                    )
                    new_show = content_manager.add(
                        tvdb_id=tvdb_id,
                        quality_profile_id=sonarr_params["sonarr_profile_id"],
                        root_dir=sonarr_params["sonarr_root"],
                        series_type=sonarr_params["series_type"],
                        season_folders=sonarr_params["season_folders"],
                    )
                    if new_show.__contains__("id"):
                        add_request_to_db(
                            content_id=tvdb_id,
                            source="tvdb",
                            user=request.user,
                        )
                        content_manager.request(
                            sonarr_id=new_show["id"],
                            seasons=request_parameters["seasons"],
                            episode_ids=request_parameters["episode_ids"],
                        )

                    # For some reason the new show did not contain an ID
                    else:
                        log.handler(
                            "Show was added to Sonarr, but Sonarr did not return an ID!",
                            log.ERROR,
                            __logger,
                        )

                # Request a show that's already within Sonarr
                else:
                    add_request_to_db(
                        content_id=tvdb_id,
                        source="tvdb",
                        user=request.user,
                    )
                    content_manager.request(
                        sonarr_id=preexisting_show["id"],
                        seasons=request_parameters["seasons"],
                        episode_ids=request_parameters["episode_ids"],
                    )

        # Movie was requested
        elif request_parameters["content_type"] == "movie":
            radarr_params = obtain_radarr_parameters(
                content_discovery, content_manager, request_parameters["tmdb_id"]
            )

            # Check if the movie is already within Radarr's collection
            preexisting_movie = content_manager.get(
                tmdb_id=request_parameters["tmdb_id"]
            )

            # If it doesn't already exists, add then request it
            if preexisting_movie is None:
                new_movie = content_manager.add(
                    tmdb_id=request_parameters["tmdb_id"],
                    quality_profile_id=radarr_params["radarr_profile_id"],
                    root_dir=radarr_params["radarr_root"],
                )
                if new_movie.__contains__("id"):
                    add_request_to_db(
                        content_id=request_parameters["tmdb_id"],
                        source="tmdb",
                        user=request.user,
                    )
                    content_manager.request(radarr_id=new_movie["id"])
                else:
                    log.handler(
                        "Movie was added to Radarr, but Radarr did not return an ID!",
                        log.ERROR,
                        __logger,
                    )

            # If it already existed, just request it
            else:
                add_request_to_db(
                    content_id=request_parameters["tmdb_id"],
                    source="tmdb",
                    user=request.user,
                )
                content_manager.request(radarr_id=preexisting_movie["id"])

    return JsonResponse({})

    # return HttpResponseForbidden()
