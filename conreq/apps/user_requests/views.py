import json

from conreq.apps.base.tasks import background_task
from conreq.apps.user_requests.models import UserRequest
from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.utils import log
from conreq.utils.apps import (
    add_unique_to_db,
    generate_context,
    obtain_radarr_parameters,
    obtain_sonarr_parameters,
)
from conreq.utils.testing import performance_metrics
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .helpers import add_save_request_movie, generate_requests_cards

# Days, Hours, Minutes, Seconds
INVITE_CODE_DURATION = 7 * 24 * 60 * 60
__logger = log.get_logger(__name__)

# Create your views here.


@login_required
@performance_metrics()
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
            tvdb_id = None
            tmdb_id = None
            if request_parameters.__contains__("tvdb_id"):
                tvdb_id = request_parameters["tvdb_id"]
            if request_parameters.__contains__("tmdb_id"):
                tmdb_id = request_parameters["tmdb_id"]

            if not tvdb_id and tmdb_id:
                tvdb_id = content_discovery.get_external_ids(tmdb_id, "tv")["tvdb_id"]

            # Request the show by the TVDB ID
            if tvdb_id:
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

                # Request
                background_task(
                    content_manager.request,
                    sonarr_id=show["id"],
                    seasons=request_parameters["seasons"],
                    episode_ids=request_parameters["episode_ids"],
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

            # Request
            background_task(
                add_save_request_movie,
                content_manager,
                tmdb_id,
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

        return JsonResponse({})

    return HttpResponseForbidden()


@cache_page(1)
@vary_on_cookie
@login_required
@performance_metrics()
def my_requests(request):
    template = loader.get_template("viewport/requests.html")
    user_requests = (
        UserRequest.objects.filter(requested_by=request.user).order_by("id").reverse()
    )
    all_cards = generate_requests_cards(user_requests)
    context = generate_context({"all_cards": all_cards})
    return HttpResponse(template.render(context, request))


@cache_page(1)
@login_required
@performance_metrics()
def all_requests(request):
    template = loader.get_template("viewport/requests.html")
    user_requests = UserRequest.objects.all().order_by("id").reverse()
    all_cards = generate_requests_cards(user_requests)
    context = generate_context({"all_cards": all_cards})
    return HttpResponse(template.render(context, request))
