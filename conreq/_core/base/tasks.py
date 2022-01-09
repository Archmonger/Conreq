import sqlite3

from django.conf import settings
from django.db import connection
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from conreq import Seconds
from conreq.utils.backup import backup_needed, backup_now
from conreq.utils.environment import get_database_type

DB_ENGINE = get_database_type()
HUEY_FILENAME = getattr(settings, "HUEY_FILENAME")


@db_periodic_task(crontab(minute="0", hour="0", day_of_week="1"))
def clean_bg_task_db():
    """Periodically performs a SQLITE vacuum on the background task database."""
    with sqlite3.connect(HUEY_FILENAME) as cursor:
        cursor.execute(
            # Only keep the 1000 latest tasks
            """DELETE FROM task
            WHERE id NOT IN (
            SELECT id
            FROM (
                SELECT id
                FROM task
                ORDER BY id DESC
                LIMIT 1000
            ) foo
            );
            """
        )
    with sqlite3.connect(HUEY_FILENAME) as cursor:
        cursor.execute("VACUUM")


if DB_ENGINE == "SQLITE3":

    @db_periodic_task(crontab(minute="0", hour="0", day_of_week="1"))
    def clean_conreq_db():
        """Periodically performs any cleanup tasks needed for the default database."""
        with connection.cursor() as cursor:
            cursor.execute("VACUUM")


@db_periodic_task(Seconds.day)
def backup_check():
    """Backup the database when needed."""
    if backup_needed():
        backup_now()
