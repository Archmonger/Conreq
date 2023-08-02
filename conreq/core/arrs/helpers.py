from conreq.core.arrs.sonarr import SonarrManager


def wait_for_series_info(tvdb_id, max_retries=10):
    """Keeps attempting to fetch a series from Sonarr until it becomes available"""
    sonarr_manager = SonarrManager()
    series = sonarr_manager.get(
        tvdb_id=tvdb_id, obtain_season_info=True, force_update_cache=True
    )
    if series is None:
        series_fetch_retries = 0
        while series is None and series_fetch_retries <= max_retries:
            series_fetch_retries += 1
            series = sonarr_manager.get(
                tvdb_id=tvdb_id, obtain_season_info=True, force_update_cache=True
            )
    return series
