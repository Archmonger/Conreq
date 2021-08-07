def wait_for_series_info(tvdb_id, sonarr_manager, max_retries=10):
    """Keeps attempting to fetch a series from Sonarr until it becomes available"""
    series = sonarr_manager.get(
        tvdb_id=tvdb_id, obtain_season_info=True, force_update_cache=True
    )
    if series is None:
        series_fetch_retries = 0
        while series is None:
            if series_fetch_retries > max_retries:
                break
            series_fetch_retries = series_fetch_retries + 1
            series = sonarr_manager.get(
                tvdb_id=tvdb_id, obtain_season_info=True, force_update_cache=True
            )
    return series
