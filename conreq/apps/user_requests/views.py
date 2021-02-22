import json

from conreq.apps.user_requests.models import UserRequest
from conreq.core.content_discovery.tmdb import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.utils import log
from conreq.utils.app_views import generate_context
from conreq.utils.testing import performance_metrics
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .helpers import generate_requests_cards, radarr_request, sonarr_request

_logger = log.get_logger(__name__)

# Days, Hours, Minutes, Seconds
INVITE_CODE_DURATION = 7 * 24 * 60 * 60


@login_required
@performance_metrics()
def request_content(request):
    # User submitted a new request
    if request.method == "POST":
        request_parameters = json.loads(request.body.decode("utf-8"))
        log.handler(
            "Request received: " + str(request_parameters),
            log.INFO,
            _logger,
        )

        content_manager = ContentManager()
        content_discovery = ContentDiscovery()

        # TV show was requested
        if request_parameters["content_type"] == "tv":
            # Try to obtain a TVDB ID (from params or fetch it from TMDB)
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
                sonarr_request(
                    tvdb_id,
                    tmdb_id,
                    request,
                    request_parameters,
                    content_manager,
                    content_discovery,
                )

            else:
                return HttpResponseForbidden()

        # Movie was requested
        elif request_parameters["content_type"] == "movie":
            tmdb_id = request_parameters["tmdb_id"]
            radarr_request(tmdb_id, request, content_manager, content_discovery)

        # The request succeeded
        return JsonResponse({"success": True})

    return HttpResponseForbidden()


@cache_page(1)
@vary_on_cookie
@login_required
@performance_metrics()
def my_requests(request):
    user_requests = (
        UserRequest.objects.filter(requested_by=request.user)
        .order_by("id")
        .reverse()
        .values()
    )
    all_cards = generate_requests_cards(user_requests)
    context = generate_context({"all_cards": all_cards})
    template = loader.get_template("viewport/requests.html")
    return HttpResponse(template.render(context, request))


@cache_page(1)
@login_required
@performance_metrics()
def all_requests(request):
    user_requests = (
        UserRequest.objects.all()
        .order_by("id")
        .reverse()
        .values(
            "content_id",
            "source",
            "content_type",
            "requested_by__username",
        )
    )
    all_cards = generate_requests_cards(user_requests)
    context = generate_context({"all_cards": all_cards})
    template = loader.get_template("viewport/requests.html")
    return HttpResponse(template.render(context, request))
