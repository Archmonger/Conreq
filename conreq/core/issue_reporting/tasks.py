from conreq.core.arrs.sonarr_radarr import ArrManager
from conreq.core.server_settings.models import ConreqConfig
from conreq.core.tmdb.discovery import TmdbDiscovery
from conreq.core.user_requests.helpers import (
    obtain_radarr_parameters,
    obtain_sonarr_parameters,
)
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from .models import ReportedIssue


@db_task()
def arr_auto_resolve_tv(tmdb_id, seasons, episode_ids, resolutions):
    """Queues a background task to automatically resolve a reported issue."""
    # Check if auto resolution is turned on
    # Delete the content then search for a replacement


@db_task()
def arr_auto_resolve_movie(tmdb_id, issue_id, resolutions):
    """Queues a background task to automatically resolve a reported issue."""
    # Check if auto resolution is turned on
    conreq_config = ConreqConfig.get_solo()
    if conreq_config.conreq_auto_resolve_issues:
        content_manager = ArrManager()
        content_discovery = TmdbDiscovery()

        # Grab the movie from Radarr
        movie = content_manager.get(force_update_cache=True, tmdb_id=tmdb_id)

        # Delete if movie if it exists
        if movie:
            content_manager.delete(radarr_id=movie["id"])

        # Add or re-add the movie
        radarr_params = obtain_radarr_parameters(
            content_discovery, content_manager, tmdb_id
        )
        movie = content_manager.add(
            tmdb_id=tmdb_id,
            quality_profile_id=radarr_params["radarr_profile_id"],
            root_dir=radarr_params["radarr_root"],
        )

        # Search for a replacement
        content_manager.request(radarr_id=movie["id"])
        issue = ReportedIssue.objects.get(pk=issue_id)
        issue.auto_resolve_in_progress = True
        issue.save()


@db_periodic_task(crontab("*/1"))
def auto_resolve_watchdog():
    """Checks to see if an auto resolution has finished completely."""
    # Check if auto resolution is turned on
    conreq_config = ConreqConfig.get_solo()
    if conreq_config.conreq_auto_resolve_issues:
        content_manager = ArrManager()
        issues = ReportedIssue.objects.select_for_update(nowait=True).filter(
            auto_resolve_in_progress=True
        )
        newly_resolved_issues = []

        for issue in issues:
            # Check if TV issues have been resolved
            if issue.content_type == "tv":
                pass

            # Check if movie issues have been resolved
            if issue.content_type == "movie":
                movie = content_manager.get(tmdb_id=issue.content_id)
                if movie and movie.get("downloaded"):
                    issue.auto_resolve_in_progress = False
                    issue.auto_resolved = True
                    issue.resolved = True
                    newly_resolved_issues.append(issue)

        # Save the resolution status
        if newly_resolved_issues:
            ReportedIssue.objects.bulk_update(
                newly_resolved_issues,
                ["auto_resolve_in_progress", "auto_resolved", "resolved"],
            )
