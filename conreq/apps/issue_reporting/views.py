import json

from channels.db import database_sync_to_async as convert_to_async
from conreq.apps.issue_reporting.models import ReportedIssue
from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.utils import log
from conreq.utils.apps import add_unique_to_db, generate_context
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

__logger = log.get_logger(__name__)

# (Issue name, Resolution)
ISSUE_LIST = [
    ("Video does not match what was expected.", ["RENAME CONTENT", "REDOWNLOAD VIDEO"]),
    ("Video does not load.", ["REDOWNLOAD VIDEO"]),
    (
        "Video does not exist or is missing.",
        ["CHANGE ROOT FOLDER", "RENAME CONTENT", "REDOWNLOAD VIDEO"],
    ),
    ("Video is in the wrong category/folder.", ["CHANGE ROOT FOLDER"]),
    ("Wrong video length.", ["REDOWNLOAD VIDEO"]),
    ("Wrong audio language.", ["REDOWNLOAD VIDEO"]),
    ("Wrong subtitle language.", ["REDOWNLOAD SUBTITLES"]),
    ("Low quality video.", ["UPGRADE VIDEO"]),
    ("Bad or corrupt video.", ["REDOWNLOAD VIDEO"]),
    ("Bad or corrupt audio.", ["REDOWNLOAD VIDEO"]),
    ("Bad subtitles.", ["REDOWNLOAD SUBTITLES"]),
    ("Missing subtitles.", ["REDOWNLOAD SUBTITLES"]),
    ("Other.", ["NOTIFY ADMIN"]),
]

# Create your views here.
@convert_to_async
@login_required
def report_issue(request):
    if request.method == "POST":
        request_parameters = json.loads(request.body.decode("utf-8"))
        log.handler(
            "Issue report received: " + str(request_parameters),
            log.INFO,
            __logger,
        )

        # Get the parameters from the response
        if request_parameters.get("tmdb_id", None):
            content_id = request_parameters.get("tmdb_id", None)
            source = "tmdb"
        elif request_parameters.get("tvdb_id", None):
            content_id = request_parameters.get("tvdb_id", None)
            source = "tvdb"
        content_type = request_parameters.get("content_type", None)
        issue_names = [ISSUE_LIST[i][0] for i in request_parameters["issue_ids"]]
        all_resolutions = [ISSUE_LIST[i][1] for i in request_parameters["issue_ids"]]
        resolutions = list(set([j for i in all_resolutions for j in i]))
        seasons = request_parameters.get("seasons", [])
        episodes = request_parameters.get("episodes", [])
        episode_ids = request_parameters.get("episode_ids", [])

        # Add the report to the database
        add_unique_to_db(
            ReportedIssue,
            issues=issue_names,
            resolutions=resolutions,
            reported_by=request.user,
            content_id=content_id,
            source=source,
            content_type=content_type,
            seasons=seasons,
            episodes=episodes,
            episode_ids=episode_ids,
        )

        return JsonResponse({"success": True})

    return HttpResponseForbidden()


@convert_to_async
@cache_page(60)
@login_required
def report_issue_modal(request):
    # Get the parameters from the URL
    context = generate_context(
        {
            "issues": ISSUE_LIST,
            "tmdb_id": request.GET.get("tmdb_id", None),
            "tvdb_id": request.GET.get("tvdb_id", None),
            "content_type": request.GET.get("content_type", None),
        }
    )
    template = loader.get_template("modal/report_issue.html")
    return HttpResponse(template.render(context, request))


@convert_to_async
@cache_page(1)
@login_required
@user_passes_test(lambda u: u.is_staff)
def all_issues(request):
    # Get the parameters from the URL
    content_discovery = ContentDiscovery()
    content_manager = ContentManager()
    reported_issues = ReportedIssue.objects.all().order_by("id").reverse()

    all_cards = []
    for entry in reported_issues.values(
        "reported_by__username",
        "content_id",
        "source",
        "resolved",
        "content_type",
        "issues",
        "seasons",
        "episodes",
    ):
        # Fetch TMDB entry
        if entry["source"] == "tmdb":
            card = content_discovery.get_by_tmdb_id(
                tmdb_id=entry["content_id"],
                content_type=entry["content_type"],
                obtain_extras=False,
            )
            if card is not None:
                card["tmdbCard"] = True
                all_cards.append({**card, **entry})

        # Fetch TVDB entry
        if entry["source"] == "tvdb":
            # Attempt to convert card to TMDB
            conversion = content_discovery.get_by_tvdb_id(tvdb_id=entry["content_id"])
            # Conversion found
            if conversion.__contains__("tv_results") and conversion["tv_results"]:
                card = conversion["tv_results"][0]
                card["tmdbCard"] = True
                all_cards.append({**card, **entry})

                # Convert all requests to use this new ID
                old_requests = ReportedIssue.objects.filter(
                    content_id=entry["content_id"], source="tvdb"
                )
                old_requests.update(content_id=card["id"], source="tmdb")

            # Fallback to checking sonarr's database
            else:
                card = content_manager.get(tvdb_id=entry["content_id"])
                all_cards.append({**card, **entry})

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

    context = generate_context({"all_cards": all_cards})
    template = loader.get_template("viewport/reported_issues.html")
    return HttpResponse(template.render(context, request))


@convert_to_async
@cache_page(1)
@vary_on_cookie
@login_required
def my_issues(request):
    # Get the parameters from the URL
    content_discovery = ContentDiscovery()
    content_manager = ContentManager()
    reported_issues = (
        ReportedIssue.objects.filter(reported_by=request.user).order_by("id").reverse()
    )

    all_cards = []
    for entry in reported_issues.values(
        "reported_by__username",
        "content_id",
        "source",
        "resolved",
        "content_type",
        "issues",
        "seasons",
        "episodes",
    ):
        # Fetch TMDB entry
        if entry["source"] == "tmdb":
            card = content_discovery.get_by_tmdb_id(
                tmdb_id=entry["content_id"],
                content_type=entry["content_type"],
                obtain_extras=False,
            )
            if card is not None:
                card["tmdbCard"] = True
                all_cards.append({**card, **entry})

        # Fetch TVDB entry
        if entry["source"] == "tvdb":
            # Attempt to convert card to TMDB
            conversion = content_discovery.get_by_tvdb_id(tvdb_id=entry["content_id"])
            # Conversion found
            if conversion.__contains__("tv_results") and conversion["tv_results"]:
                card = conversion["tv_results"][0]
                card["tmdbCard"] = True
                all_cards.append({**card, **entry})

                # Convert all requests to use this new ID
                old_requests = ReportedIssue.objects.filter(
                    content_id=entry["content_id"], source="tvdb"
                )
                old_requests.update(content_id=card["id"], source="tmdb")

            # Fallback to checking sonarr's database
            else:
                card = content_manager.get(tvdb_id=entry["content_id"])
                all_cards.append({**card, **entry})

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

    context = generate_context({"all_cards": all_cards})
    template = loader.get_template("viewport/reported_issues.html")
    return HttpResponse(template.render(context, request))
