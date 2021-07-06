from huey.contrib.djhuey import db_task


@db_task()
def arr_auto_resolve_tv(tmdb_id, seasons, episode_ids, resolutions):
    """Queues a background task to automatically resolve a reported issue."""
    # Check if auto resolution is turned on
    # Delete the content then search for a replacement


@db_task()
def arr_auto_resolve_movie(tmdb_id, resolutions):
    """Queues a background task to automatically resolve a reported issue."""
    # Check if auto resolution is turned on
    # Delete the content then search for a replacement
