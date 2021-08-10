from conreq.core.arrs.helpers import wait_for_series_info
from conreq.core.arrs.sonarr import SonarrManager
from conreq.core.tmdb.discovery import TmdbDiscovery
from conreq.core.user_requests.models import UserRequest
from conreq.utils import log
from conreq.utils.generic import is_key_value_in_list, str_to_bool
from conreq.utils.debug import performance_metrics
from conreq.utils.views import (
    obtain_sonarr_parameters,
    set_many_availability,
    set_single_availability,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.views.decorators.cache import cache_page

from .helpers import preprocess_tmdb_person, preprocess_tmdb_result

_logger = log.get_logger(__name__)

# Globals
MAX_SERIES_FETCH_RETRIES = 10


@cache_page(15)
@login_required
@performance_metrics()
def more_info(request):
    content_discovery = TmdbDiscovery()
    template = loader.get_template("viewport/more_info.html")

    # Get the ID from the URL
    tmdb_id = request.GET.get("tmdb_id", None)
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

    # Render the page
    return HttpResponse(template.render(context, request))


@cache_page(7 * 24 * 60 * 60)
@login_required
@performance_metrics()
def person(request):
    content_discovery = TmdbDiscovery()
    template = loader.get_template("viewport/person.html")
    context = {}

    # Get the ID from the URL
    person_id = request.GET.get("id", None)

    # Fetch the person from TMDB
    if person_id:
        results = content_discovery.person(person_id)

        # Preprocessing before passing into HTML
        preprocess_tmdb_person(results)
        if results["tv_credits"]["cast"]:
            content_discovery.determine_id_validity(results["tv_credits"]["cast"])
            set_many_availability(results["tv_credits"]["cast"])
        if results["tv_credits"]["crew"]:
            content_discovery.determine_id_validity(results["tv_credits"]["crew"])
            set_many_availability(results["tv_credits"]["crew"])
        if results["movie_credits"]["cast"]:
            content_discovery.determine_id_validity(results["movie_credits"]["cast"])
            set_many_availability(results["movie_credits"]["cast"])
        if results["movie_credits"]["crew"]:
            content_discovery.determine_id_validity(results["movie_credits"]["crew"])
            set_many_availability(results["movie_credits"]["crew"])
        tv_cast_contain_valid_id = is_key_value_in_list(
            "conreq_valid_id", True, results["tv_credits"]["cast"]
        )
        tv_crew_contain_valid_id = is_key_value_in_list(
            "conreq_valid_id", True, results["tv_credits"]["crew"]
        )
        if results.get("popularity"):
            results["popularity"] = int(results["popularity"] * 10)

        # Generate context for page rendering
        context = {
            "person": results,
            "tv_cast_contain_valid_id": tv_cast_contain_valid_id,
            "tv_crew_contain_valid_id": tv_crew_contain_valid_id,
        }

    # Render the page
    return HttpResponse(template.render(context, request))


@cache_page(15)
@login_required
@performance_metrics()
def series_modal(request):
    content_discovery = TmdbDiscovery()
    sonarr_manager = SonarrManager()
    report_modal = str_to_bool(request.GET.get("report_modal", "false"))

    # Get the ID from the URL
    tmdb_id = request.GET.get("tmdb_id", None)
    tvdb_id = content_discovery.get_external_ids(tmdb_id, "tv").get("tvdb_id")

    # Check if the show is already within Sonarr's collection
    requested_show = sonarr_manager.get(tvdb_id=tvdb_id)

    # If it doesn't already exists, add then add it
    if requested_show is None:

        sonarr_params = obtain_sonarr_parameters(tmdb_id, tvdb_id)

        requested_show = sonarr_manager.add(
            tvdb_id=tvdb_id,
            quality_profile_id=sonarr_params["sonarr_profile_id"],
            root_dir=sonarr_params["sonarr_root"],
            series_type=sonarr_params["series_type"],
            season_folders=sonarr_params["season_folders"],
        )

    # Keep refreshing until we get the series from Sonarr
    series = wait_for_series_info(tvdb_id)

    # Series successfully obtained from Sonarr
    if series:
        context = {
            "seasons": series["seasons"],
            "tmdb_id": tmdb_id,
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
    content_discovery = TmdbDiscovery()

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
        content_discovery = TmdbDiscovery()

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
        content_discovery = TmdbDiscovery()

        tmdb_collection = content_discovery.collections(collection_id)

        if not isinstance(tmdb_collection, dict) or not tmdb_collection:
            tmdb_collection = None

        else:
            set_many_availability(tmdb_collection["parts"])

        context = {"collection": tmdb_collection}
        template = loader.get_template("viewport/components/more_info_collection.html")
        return HttpResponse(template.render(context, request))
