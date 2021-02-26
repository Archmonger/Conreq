import json

from conreq.apps.issue_reporting.models import ReportedIssue
from conreq.utils import log
from conreq.utils.app_views import add_unique_to_db
from conreq.utils.testing import performance_metrics
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .helpers import ISSUE_LIST, generate_issue_cards

_logger = log.get_logger(__name__)


@login_required
@performance_metrics()
def report_issue(request):
    if request.method == "POST":
        request_parameters = json.loads(request.body.decode("utf-8"))
        log.handler(
            "Issue report received: " + str(request_parameters),
            log.INFO,
            _logger,
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


@login_required
@performance_metrics()
def manage_issue(request):
    if request.method == "POST":
        request_parameters = json.loads(request.body.decode("utf-8"))
        log.handler(
            "Manage issue command received: " + str(request_parameters),
            log.INFO,
            _logger,
        )

        # Delete a request
        if request_parameters.get("action", None) == "delete":
            issue = ReportedIssue.objects.select_related("reported_by").get(
                id=request_parameters["request_id"]
            )

            # Check if report belongs to the user, or if the user is admin
            if issue and request.user.is_staff or issue.reported_by == request.user:
                issue.delete()
                return JsonResponse({"success": True})

        # Change the resolved status of a request
        elif (
            request_parameters.get("action", None) == "resolve"
            and request.user.is_staff
        ):
            issue = ReportedIssue.objects.filter(id=request_parameters["request_id"])
            if issue:
                issue.update(resolved=request_parameters["resolved"])
                return JsonResponse({"success": True})

    return HttpResponseForbidden()


@cache_page(15)
@login_required
@performance_metrics()
def report_issue_modal(request):
    # Get the parameters from the URL
    context = {
        "issues": ISSUE_LIST,
        "tmdb_id": request.GET.get("tmdb_id", None),
        "tvdb_id": request.GET.get("tvdb_id", None),
        "content_type": request.GET.get("content_type", None),
    }
    template = loader.get_template("modal/report_issue.html")
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(lambda u: u.is_staff)
@performance_metrics()
def all_issues(request):
    reported_issues = ReportedIssue.objects.all().order_by("id").reverse()
    all_cards = generate_issue_cards(reported_issues)
    context = {"all_cards": all_cards}
    template = loader.get_template("viewport/reported_issues.html")
    return HttpResponse(template.render(context, request))


@vary_on_cookie
@login_required
@performance_metrics()
def my_issues(request):
    reported_issues = (
        ReportedIssue.objects.filter(reported_by=request.user).order_by("id").reverse()
    )
    all_cards = generate_issue_cards(reported_issues)
    context = {"all_cards": all_cards}
    template = loader.get_template("viewport/reported_issues.html")
    return HttpResponse(template.render(context, request))
