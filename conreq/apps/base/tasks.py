from huey import crontab
from huey.contrib.djhuey import periodic_task, db_task
from conreq.core.content_manager import ContentManager


@db_task()
@periodic_task(crontab(minute="*/1"))
def refresh_content():
    """Checks Sonarr/Radarr for new entries every minute."""
    ContentManager().refresh_content()
