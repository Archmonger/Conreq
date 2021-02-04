from threading import Thread
from time import sleep

from conreq.apps.user_requests.models import UserRequest
from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.core.content_search import Search
from conreq.utils import log
from conreq.utils.apps import (
    generate_context,
    obtain_sonarr_parameters,
    preprocess_arr_result,
    preprocess_tmdb_result,
    set_many_conreq_status,
    set_single_conreq_status,
)
from conreq.utils.generic import ReturnThread
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page

# Globals
MAX_SERIES_FETCH_RETRIES = 20

__logger = log.get_logger(__name__)

# Create your views here.
@cache_page(60)
@login_required
def more_info(request):
    content_discovery = ContentDiscovery()
    template = loader.get_template("viewport/more_info.html")
    thread_list = []

    # Get the ID from the URL
    tmdb_id = request.GET.get("tmdb_id", None)
    tvdb_id = request.GET.get("tvdb_id", None)

    if tmdb_id:
        content_type = request.GET.get("content_type", None)

        # Get all the basic metadata for a given ID
        content = content_discovery.get_by_tmdb_id(tmdb_id, content_type)

        # Get recommended results
        similar_and_recommended_thread = ReturnThread(
            target=content_discovery.similar_and_recommended,
            args=[tmdb_id, content_type],
        )
        similar_and_recommended_thread.start()

        # Checking Conreq status of the current TMDB ID
        thread = Thread(target=set_single_conreq_status, args=[content])
        thread.start()
        thread_list.append(thread)

        # Pre-process data attributes within tmdb_result
        thread = Thread(target=preprocess_tmdb_result, args=[content])
        thread.start()
        thread_list.append(thread)

        # Get collection information
        if (
            content.__contains__("belongs_to_collection")
            and content["belongs_to_collection"] is not None
        ):
            tmdb_collection = True
            tmdb_collection_thread = ReturnThread(
                target=content_discovery.collections,
                args=[content["belongs_to_collection"]["id"]],
            )
            tmdb_collection_thread.start()
        else:
            tmdb_collection = None

        # Recommended content
        tmdb_recommended = similar_and_recommended_thread.join()
        if not isinstance(tmdb_recommended, dict) or len(tmdb_recommended) == 0:
            tmdb_recommended = None

        # Checking Conreq status for all recommended content
        thread = Thread(
            target=set_many_conreq_status, args=[tmdb_recommended["results"]]
        )
        thread.start()
        thread_list.append(thread)

        # Wait for thread computation to complete
        for thread in thread_list:
            thread.join()
        if tmdb_collection is not None:
            tmdb_collection = tmdb_collection_thread.join()

        # Check if the user has already requested this
        requested = False
        if UserRequest.objects.filter(
            content_id=content["id"],
            source="tmdb",
            content_type=content["content_type"],
        ):
            requested = True

        # Generate context for page rendering
        context = generate_context(
            {
                "content": content,
                "recommended": tmdb_recommended,
                "collection": tmdb_collection,
                "content_type": content["content_type"],
                "requested": requested,
            }
        )

    elif tvdb_id:
        searcher = Search()
        # Fallback for TVDB
        content = searcher.television(tvdb_id)[0]
        thread_list = []

        # Preprocess results
        thread = Thread(target=preprocess_arr_result, args=[content])
        thread.start()
        thread_list.append(thread)

        # Obtain conreq status
        thread = Thread(target=set_single_conreq_status, args=[content])
        thread.start()
        thread_list.append(thread)

        # Wait for thread computation to complete
        for thread in thread_list:
            thread.join()

        # Generate context for page rendering
        context = generate_context(
            {
                "content": content,
                "content_type": content["contentType"],
            }
        )

    # Render the page
    return HttpResponse(template.render(context, request))


@cache_page(60)
@login_required
def series_modal(request):
    content_discovery = ContentDiscovery()
    content_manager = ContentManager()
    report_modal = request.GET.get("report_modal", False)

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
    series = content_manager.get(tvdb_id=tvdb_id, obtain_season_info=True)
    if series is None:
        series_fetch_retries = 0
        while series is None:
            if series_fetch_retries > MAX_SERIES_FETCH_RETRIES:
                break
            series_fetch_retries = series_fetch_retries + 1
            sleep(0.5)
            series = content_manager.get(
                tvdb_id=tvdb_id, obtain_season_info=True, force_update_cache=True
            )
            log.handler(
                "Sonarr did not have the series information! Conreq is waiting...",
                log.INFO,
                __logger,
            )

    context = generate_context(
        {"seasons": series["seasons"], "tvdb_id": tvdb_id, "report_modal": report_modal}
    )
    template = loader.get_template("modal/series_selection.html")
    return HttpResponse(template.render(context, request))


@cache_page(60)
@login_required
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
        set_single_conreq_status(content)
        preprocess_tmdb_result(content)

        # Check if the user has already requested this
        requested = False
        if UserRequest.objects.filter(
            content_id=content["id"],
            source="tmdb",
            content_type=content["content_type"],
        ):
            requested = True

        context = generate_context({"content": content, "requested": requested})
        template = loader.get_template("modal/content_preview.html")
        return HttpResponse(template.render(context, request))
