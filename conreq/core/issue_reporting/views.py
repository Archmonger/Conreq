import json

from conreq.core.issue_reporting.models import ReportedIssue
from conreq.utils import log
from conreq.utils.database import add_unique_to_db
from conreq.utils.debug import performance_metrics
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .helpers import ISSUE_LIST, generate_issue_cards
from .tasks import arr_auto_resolve_movie, arr_auto_resolve_tv

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
        all_resolutions = [ISSUE_LIST[i][1] for i in request_parameters["issue_ids"]]
        params = {
            "reported_by": request.user,
            "content_id": request_parameters.get("tmdb_id", None),
            "content_type": request_parameters.get("content_type", None),
            "issues": [ISSUE_LIST[i][0] for i in request_parameters["issue_ids"]],
            "resolutions": list(set([j for i in all_resolutions for j in i])),
            "seasons": request_parameters.get("seasons", []),
            "episodes": request_parameters.get("episodes", []),
            "episode_ids": request_parameters.get("episode_ids", []),
        }

        # Add the report to the database
        new_issue = add_unique_to_db(ReportedIssue, **params)

        # Auto resolve
        if new_issue and params["content_type"] == "tv":
            arr_auto_resolve_tv(
                new_issue.pk,
                params["content_id"],
                params["seasons"],
                params["episode_ids"],
                params["resolutions"],
            )
        elif new_issue and params["content_type"] == "movie":
            arr_auto_resolve_movie(
                new_issue.pk, params["content_id"], params["resolutions"]
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
                issue.update(
                    resolved=request_parameters["resolved"],
                    auto_resolved=False,
                    auto_resolve_in_progress=False,
                )
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
        "content_type": request.GET.get("content_type", None),
    }
    template = loader.get_template("modal/report_issue.html")
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(lambda u: u.is_staff)
@performance_metrics()
def all_issues(request):
    reported_issues = (
        ReportedIssue.objects.all()
        .order_by("id")
        .reverse()
        .values(
            "id",
            "reported_by__username",
            "content_id",
            "resolved",
            "auto_resolved",
            "auto_resolve_in_progress",
            "date_reported",
            "content_type",
            "issues",
            "seasons",
            "episodes",
        )
    )
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(reported_issues, 25)
    page_obj = paginator.get_page(page_number)
    if page_number <= paginator.num_pages:
        all_cards = generate_issue_cards(page_obj)
    else:
        all_cards = None
    context = {"all_cards": all_cards, "page_name": "All Issues"}
    template = loader.get_template("viewport/reported_issues.html")
    return HttpResponse(template.render(context, request))


@vary_on_cookie
@login_required
@performance_metrics()
def my_issues(request):
    reported_issues = (
        ReportedIssue.objects.filter(reported_by=request.user)
        .order_by("id")
        .reverse()
        .values(
            "id",
            "reported_by__username",
            "content_id",
            "resolved",
            "auto_resolved",
            "auto_resolve_in_progress",
            "date_reported",
            "content_type",
            "issues",
            "seasons",
            "episodes",
        )
    )
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(reported_issues, 25)
    page_obj = paginator.get_page(page_number)
    if page_number <= paginator.num_pages:
        all_cards = generate_issue_cards(page_obj)
    else:
        all_cards = None
    context = {"all_cards": all_cards, "page_name": "My Issues"}
    template = loader.get_template("viewport/reported_issues.html")
    return HttpResponse(template.render(context, request))
