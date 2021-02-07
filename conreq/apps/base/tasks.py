from conreq.core.content_manager import ContentManager
from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task


@db_periodic_task(crontab(minute="*/1"))
def refresh_content():
    """Checks Sonarr/Radarr for new entries every minute."""
    ContentManager().refresh_content()


@db_task()
def background_task(function, *args, **kwargs):
    """Adds any function to the background task queue."""
    function(*args, **kwargs)
