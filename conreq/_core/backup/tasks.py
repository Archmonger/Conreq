from huey.contrib.djhuey import db_periodic_task, db_task

from conreq.types import Seconds
from conreq.utils.backup import backup_needed, backup_now


@db_periodic_task(Seconds.day)
def backup_check():
    """Backup the database on a schedule."""
    if backup_needed():
        backup_now()


@db_task()
def backup_if_needed():
    """Performs a backup if the last backup was longer than the threshold."""
    if backup_needed():
        backup_now()
