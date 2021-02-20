import os

from conreq.core.content_manager import ContentManager
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

ARR_REFRESH_INTERNAL = os.environ.get("ARR_REFRESH_INTERNAL", "*/1")


@db_periodic_task(crontab(minute=ARR_REFRESH_INTERNAL))
def refresh_content():
    """Checks Sonarr/Radarr for new entries every minute."""
    ContentManager().refresh_content()


@db_task()
def background_task(function, *args, **kwargs):
    """Adds any function to the background task queue."""
    function(*args, **kwargs)
