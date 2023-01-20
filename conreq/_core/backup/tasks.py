from huey.contrib.djhuey import db_periodic_task

from conreq.types import Seconds
from conreq.utils.backup import backup_needed, backup_now


@db_periodic_task(Seconds.day)
def backup_check():
    """Backup the database when needed."""
    if backup_needed():
        backup_now()
