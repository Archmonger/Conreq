from conreq.utils.generic import get_str_from_env
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from .sonarr_radarr import ArrManager

ARR_REFRESH_INTERNAL = get_str_from_env("ARR_REFRESH_INTERNAL", "*/1")


@db_periodic_task(crontab(minute=ARR_REFRESH_INTERNAL))
def refresh_content():
    """Checks Sonarr/Radarr for new entries every minute."""
    ArrManager().refresh_content()
