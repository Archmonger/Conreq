from conreq.apps.user_requests.models import UserRequest
from conreq.core.content_discovery.tmdb import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.core.content_search import Search
from conreq.utils import log
from conreq.utils.app_views import (
    obtain_sonarr_parameters,
    set_many_availability,
    set_single_availability,
)
from conreq.utils.generic import is_key_value_in_list, str_to_bool
from conreq.utils.testing import performance_metrics
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.views.decorators.cache import cache_page

from .helpers import preprocess_arr_result, preprocess_tmdb_result

_logger = log.get_logger(__name__)

# Globals
MAX_SERIES_FETCH_RETRIES = 10


@cache_page(15)
@login_required
@performance_metrics()
def more_info(request):
    content_discovery = ContentDiscovery()
    template = loader.get_template("viewport/more_info.html")

    # Get the ID from the URL
    tmdb_id = request.GET.get("tmdb_id", None)
    tvdb_id = request.GET.get("tvdb_id", None)

    if tmdb_id:
        content_type = request.GET.get("content_type", None)

        # Get all the basic metadata for a given ID
        content = content_discovery.get_by_tmdb_id(tmdb_id, content_type)

        # Determine the availability of the current TMDB ID
        set_single_availability(content)

        # Pre-process data attributes within tmdb_result
        preprocess_tmdb_result(content)

        # Get collection information
        if (
            content.__contains__("belongs_to_collection")
            and content["belongs_to_collection"] is not None
        ):
            tmdb_collection_id = content["belongs_to_collection"]["id"]
        else:
            tmdb_collection_id = None

        # Check if the user has already requested this
        requested = False
        if UserRequest.objects.filter(
            content_id=content["id"],
            source="tmdb",
            content_type=content["content_type"],
        ):
            requested = True

        # Generate context for page rendering
        context = {
            "content": content,
            "collection_id": tmdb_collection_id,
            "content_type": content["content_type"],
            "requested": requested,
        }

    elif tvdb_id:
        searcher = Search()
        # Fallback for TVDB
        content = searcher.television(tvdb_id)[0]

        # Preprocess results
        preprocess_arr_result(content)

        # Determine the availability
        set_single_availability(content)

        # Generate context for page rendering
        context = {
            "content": content,
            "content_type": content["content_type"],
        }

    # Render the page
    return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def series_modal(request):
    content_discovery = ContentDiscovery()
    content_manager = ContentManager()
    report_modal = str_to_bool(request.GET.get("report_modal", "false"))

    # Get the ID from the URL
    tmdb_id = request.GET.get("tmdb_id", None)
    tvdb_id = request.GET.get("tvdb_id", None)

    # Determine the TVDB ID
    if tvdb_id:
        pass

    elif tmdb_id:
        tvdb_id = content_discovery.get_external_ids(tmdb_id, "tv")["tvdb_id"]

    # Check if the show is already within Sonarr's collection
    requested_show = content_manager.get(tvdb_id=tvdb_id)

    # If it doesn't already exists, add then add it
    if requested_show is None:

        sonarr_params = obtain_sonarr_parameters(
            content_discovery, content_manager, tmdb_id, tvdb_id
        )

        requested_show = content_manager.add(
            tvdb_id=tvdb_id,
            quality_profile_id=sonarr_params["sonarr_profile_id"],
            root_dir=sonarr_params["sonarr_root"],
            series_type=sonarr_params["series_type"],
            season_folders=sonarr_params["season_folders"],
        )

    # Keep refreshing until we get the series from Sonarr
    series = content_manager.get(
        tvdb_id=tvdb_id, obtain_season_info=True, force_update_cache=True
    )
    if series is None:
        series_fetch_retries = 0
        while series is None:
            if series_fetch_retries > MAX_SERIES_FETCH_RETRIES:
                break
            series_fetch_retries = series_fetch_retries + 1
            series = content_manager.get(
                tvdb_id=tvdb_id, obtain_season_info=True, force_update_cache=True
            )
            log.handler(
                "Sonarr did not have the series information! Conreq is waiting...",
                log.INFO,
                _logger,
            )

    # Series successfully obtained from Sonarr
    if series:
        context = {
            "seasons": series["seasons"],
            "tvdb_id": tvdb_id,
            "report_modal": report_modal,
        }
        template = loader.get_template("modal/series_selection.html")
        return HttpResponse(template.render(context, request))

    # Sonarr couldn't process this request
    return HttpResponseNotFound()


@cache_page(15)
@login_required
@performance_metrics()
def content_preview_modal(request):
    content_discovery = ContentDiscovery()

    # Get the ID from the URL
    tmdb_id = request.GET.get("tmdb_id", None)
    content_type = request.GET.get("content_type", None)

    if tmdb_id and content_type:
        # Fetch and process
        content = content_discovery.get_by_tmdb_id(
            tmdb_id, content_type, obtain_extras=False
        )
        set_single_availability(content)
        preprocess_tmdb_result(content)

        # Check if the user has already requested this
        requested = False
        if UserRequest.objects.filter(
            content_id=content["id"],
            source="tmdb",
            content_type=content["content_type"],
        ):
            requested = True

        context = {"content": content, "requested": requested}
        template = loader.get_template("modal/content_preview.html")
        return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def recommended(request):
    tmdb_id = request.GET.get("tmdb_id", None)
    content_type = request.GET.get("content_type", None)
    if tmdb_id and content_type:
        content_discovery = ContentDiscovery()

        tmdb_recommended = content_discovery.similar_and_recommended(
            tmdb_id, content_type
        )

        if not isinstance(tmdb_recommended, dict) or not tmdb_recommended:
            tmdb_recommended = None

        else:
            set_many_availability(tmdb_recommended["results"])

        # Detect situation where all results don't have TVDB IDs
        results_contain_valid_id = False
        if is_key_value_in_list("conreq_valid_id", True, tmdb_recommended["results"]):
            results_contain_valid_id = True

        context = {
            "recommended": tmdb_recommended,
            "results_contain_valid_id": results_contain_valid_id,
        }

        template = loader.get_template("viewport/components/more_info_recommended.html")
        return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def collection(request):
    collection_id = request.GET.get("collection_id", None)

    if collection_id:
        content_discovery = ContentDiscovery()

        tmdb_collection = content_discovery.collections(collection_id)

        if not isinstance(tmdb_collection, dict) or not tmdb_collection:
            tmdb_collection = None

        else:
            set_many_availability(tmdb_collection["parts"])

        context = {"collection": tmdb_collection}
        template = loader.get_template("viewport/components/more_info_collection.html")
        return HttpResponse(template.render(context, request))
