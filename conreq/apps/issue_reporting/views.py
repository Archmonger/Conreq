import json

from conreq.apps.issue_reporting.models import ReportedIssue
from conreq.utils import log
from conreq.utils.apps import add_unique_to_db, generate_context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page

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
    ("Bad or corrupt video.", ["REDOWNLOAD VIDEO"]),
    ("Bad or corrupt audio.", ["REDOWNLOAD VIDEO"]),
    ("Bad subtitles.", ["REDOWNLOAD SUBTITLES"]),
    ("Missing subtitles.", ["REDOWNLOAD SUBTITLES"]),
    ("Other.", ["NOTIFY ADMIN"]),
]

# Create your views here.
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
        issue_names = json.dumps(
            [ISSUE_LIST[i][0] for i in request_parameters["issue_ids"]]
        )
        all_resolutions = [ISSUE_LIST[i][1] for i in request_parameters["issue_ids"]]
        resolutions = json.dumps(list(set([j for i in all_resolutions for j in i])))
        seasons = json.dumps(request_parameters.get("seasons", []))
        episode_ids = json.dumps(request_parameters.get("episode_ids", []))

        # Add the report to the database
        add_unique_to_db(
            ReportedIssue,
            names=issue_names,
            resolutions=resolutions,
            reported_by=request.user,
            content_id=content_id,
            source=source,
            content_type=content_type,
            seasons=seasons,
            episode_ids=episode_ids,
        )

        return JsonResponse({"success": True})

    return HttpResponseForbidden()


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
