from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager
from conreq.utils.apps import generate_context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page

# (Issue name, Resolution)
ISSUE_LIST = [
    ("Video does not match what was requested.", "REDOWNLOAD VIDEO"),
    ("Video does not load.", "REDOWNLOAD VIDEO"),
    ("Video does not exist.", "REMOVE THEN REDOWNLOAD VIDEO"),
    ("Video is in the wrong category/folder.", "CHANGE ROOT FOLDER"),
    ("Wrong video length.", "REDOWNLOAD VIDEO"),
    ("Wrong audio language.", "REDOWNLOAD VIDEO"),
    ("Wrong subtitle language.", "REDOWNLOAD SUBTITLES"),
    ("Bad or corrupt video.", "REDOWNLOAD VIDEO"),
    ("Bad or corrupt audio.", "REDOWNLOAD VIDEO"),
    ("Bad subtitles.", "REDOWNLOAD SUBTITLES"),
    ("Missing subtitles.", "REDOWNLOAD SUBTITLES"),
    ("Other:", "NOTIFY ADMIN"),
]

# Create your views here.
@login_required
def report_issue(request):
    content_discovery = ContentDiscovery()

    # Get the ID from the URL
    tmdb_id = request.GET.get("tmdb_id", None)
    tvdb_id = request.GET.get("tvdb_id", None)
    content_type = request.GET.get("content_type", None)

    if tmdb_id and content_type:
        pass

    elif tvdb_id and content_type:
        pass

    context = generate_context({})
    template = loader.get_template("modal/report_issue.html")
    return HttpResponse(template.render(context, request))


@login_required
def report_issue_modal(request):
    content_discovery = ContentDiscovery()

    # Get the ID from the URL
    tmdb_id = request.GET.get("tmdb_id", None)
    tvdb_id = request.GET.get("tvdb_id", None)
    content_type = request.GET.get("content_type", None)

    if tmdb_id and content_type:
        # Fetch and process
        content = content_discovery.get_by_tmdb_id(
            tmdb_id, content_type, obtain_extras=False
        )

    elif tvdb_id and content_type:
        pass

    context = generate_context({"issues": ISSUE_LIST})
    template = loader.get_template("modal/report_issue.html")
    return HttpResponse(template.render(context, request))
