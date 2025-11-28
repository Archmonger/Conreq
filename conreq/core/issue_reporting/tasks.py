from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from conreq.core.arrs.helpers import wait_for_series_info
from conreq.core.arrs.radarr import RadarrManager
from conreq.core.arrs.sonarr import SonarrManager
from conreq.core.server_settings.models import ConreqConfig
from conreq.core.tmdb.discovery import TmdbDiscovery
from conreq.core.user_requests.helpers import (
    obtain_radarr_parameters,
    obtain_sonarr_parameters,
)

from .models import ReportedIssue


@db_task(expires=120)
def arr_auto_resolve_tv(issue_id, tmdb_id, seasons, episode_ids, resolutions):
    """Queues a background task to automatically resolve a reported issue."""
    # TODO: Intelligently resolve based on "resolutions"
    # Check if auto resolution is turned on
    conreq_config = ConreqConfig.get_solo()
    if conreq_config.conreq_auto_resolve_issues:
        sonarr_manager = SonarrManager()
        content_discovery = TmdbDiscovery()
        tvdb_id = content_discovery.get_external_ids(tmdb_id, "tv").get("tvdb_id")

        # Grab the show from Sonarr
        show = sonarr_manager.get(
            force_update_cache=True, obtain_season_info=True, tvdb_id=tvdb_id
        )

        # Show doesn't exist, add it
        if not show:
            # Add the show
            sonarr_params = obtain_sonarr_parameters(tmdb_id=tmdb_id)
            show = sonarr_manager.add(
                tvdb_id=tvdb_id,
                quality_profile_id=sonarr_params["sonarr_profile_id"],
                root_dir=sonarr_params["sonarr_root"],
                series_type=sonarr_params["series_type"],
                season_folders=sonarr_params["season_folders"],
            )

        # Show already exists, handle whole show
        if show and not seasons and not episode_ids:
            # Delete the whole show
            sonarr_manager.delete(sonarr_id=show.get("id"))

            # Re-add the show
            sonarr_params = obtain_sonarr_parameters(tmdb_id=tmdb_id, tvdb_id=tvdb_id)
            show = sonarr_manager.add(
                tvdb_id=tvdb_id,
                quality_profile_id=sonarr_params["sonarr_profile_id"],
                root_dir=sonarr_params["sonarr_root"],
                series_type=sonarr_params["series_type"],
                season_folders=sonarr_params["season_folders"],
            )

        # Show already exists, handle individual seasons/episodes
        if show and seasons or episode_ids:
            # Obtain the seasons and episodes
            for season in show.get("seasons", []):
                for episode in season.get("episodes"):
                    if (
                        # User reported an episode, check if the episode has a file
                        episode.get("id") in episode_ids and episode.get("hasFile")
                    ) or (
                        # User reported a season, check if the season has episode files to be deleted
                        season.get("seasonNumber") in seasons and episode.get("hasFile")
                    ):
                        sonarr_manager.delete_episode(
                            episode_file_id=episode.get("episodeFileId")
                        )

        # Keep refreshing until we get the series from Sonarr
        show = wait_for_series_info(tvdb_id)

        # Download new copies
        sonarr_manager.request(
            sonarr_id=show.get("id"), seasons=seasons, episode_ids=episode_ids
        )
        issue = ReportedIssue.objects.get(pk=issue_id)
        issue.auto_resolve_in_progress = True
        issue.save()


@db_task(expires=120)
def arr_auto_resolve_movie(issue_id, tmdb_id, resolutions):
    """Queues a background task to automatically resolve a reported issue."""
    # TODO: Intelligently resolve based on "resolutions"
    # Check if auto resolution is turned on
    conreq_config = ConreqConfig.get_solo()
    if conreq_config.conreq_auto_resolve_issues:
        radarr_manager = RadarrManager()

        # Grab the movie from Radarr
        movie = radarr_manager.get(force_update_cache=True, tmdb_id=tmdb_id)

        # Delete if movie if it exists
        if movie:
            radarr_manager.delete(radarr_id=movie["id"])

        # Add or re-add the movie
        radarr_params = obtain_radarr_parameters(tmdb_id)
        movie = radarr_manager.add(
            tmdb_id=tmdb_id,
            quality_profile_id=radarr_params["radarr_profile_id"],
            root_dir=radarr_params["radarr_root"],
        )

        # Search for a replacement
        radarr_manager.request(radarr_id=movie["id"])
        issue = ReportedIssue.objects.get(pk=issue_id)
        issue.auto_resolve_in_progress = True
        issue.save()


@db_periodic_task(crontab(minute="*/1", strict=True), expires=120)
def auto_resolve_completion_watchdog():
    """Checks to see if an auto resolution has finished completely."""
    # Check if auto resolution is turned on
    conreq_config = ConreqConfig.get_solo()
    if conreq_config.conreq_auto_resolve_issues:
        sonarr_manager = SonarrManager()
        radarr_manager = RadarrManager()
        issues = ReportedIssue.objects.filter(auto_resolve_in_progress=True)
        newly_resolved_issues = []

        for issue in issues:
            # Check if TV issues have been resolved
            if issue.content_type == "tv":
                content_discovery = TmdbDiscovery()
                tvdb_id = content_discovery.get_external_ids(
                    issue.content_id, "tv"
                ).get("tvdb_id")
                show = sonarr_manager.get(tvdb_id=tvdb_id)
                if show and show.get("availability") == "available":
                    issue.auto_resolve_in_progress = False
                    issue.auto_resolved = True
                    issue.resolved = True
                    newly_resolved_issues.append(issue)

            # Check if movie issues have been resolved
            if issue.content_type == "movie":
                movie = radarr_manager.get(tmdb_id=issue.content_id)
                if movie and movie.get("hasFile"):
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
