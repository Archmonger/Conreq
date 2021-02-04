import json

from conreq.utils import log
from conreq.utils.apps import generate_context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
    ("Other:", ["NOTIFY ADMIN"]),
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
        tmdb_id = request_parameters.get("tmdb_id", None)
        tvdb_id = request_parameters.get("tvdb_id", None)
        content_type = request_parameters.get("content_type", None)

        if tmdb_id and content_type:
            pass

        elif tvdb_id and content_type:
            pass

        context = generate_context({})
        template = loader.get_template("modal/report_issue.html")
        return HttpResponse(template.render(context, request))


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
