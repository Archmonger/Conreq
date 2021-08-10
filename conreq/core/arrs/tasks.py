from conreq.utils.environment import get_str_from_env
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from .radarr import RadarrManager
from .sonarr import SonarrManager

ARR_REFRESH_INTERNAL = get_str_from_env("ARR_REFRESH_INTERNAL", "*/1")


@db_periodic_task(crontab(minute=ARR_REFRESH_INTERNAL))
def refresh_radarr_library():
    """Checks Radarr for new entries."""
    RadarrManager().refresh_library()


@db_periodic_task(crontab(minute=ARR_REFRESH_INTERNAL))
def refresh_sonarr_library():
    """Checks Sonarr for new entries."""
    SonarrManager().refresh_library()
