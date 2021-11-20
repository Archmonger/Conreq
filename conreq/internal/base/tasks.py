import sqlite3

from django.conf import settings
from django.core.management import call_command
from django.db import connection
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from conreq.utils.environment import get_database_type
from conreq.utils.time import Seconds

DB_ENGINE = get_database_type()
HUEY_FILENAME = getattr(settings, "HUEY_FILENAME")


@db_periodic_task(crontab(minute="0", hour="0"))
def clean_bg_task_db():
    """Periodically performs a SQLITE vacuum on the background task database."""
    if HUEY_FILENAME.exists():
        with sqlite3.connect(HUEY_FILENAME) as cursor:
            cursor.execute("VACUUM")
            cursor.execute("PRAGMA optimize")


if DB_ENGINE == "SQLITE3":

    @db_periodic_task(crontab(minute="0", hour="0"))
    def clean_conreq_db():
        """Periodically performs any cleanup tasks needed for the default database."""
        with connection.cursor() as cursor:
            cursor.execute("VACUUM")
            cursor.execute("PRAGMA optimize")


@db_periodic_task(Seconds.week)
def backup_conreq_db():
    """Backup the database once a week."""
    call_command("dbbackup", "--clean")
