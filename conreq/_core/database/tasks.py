import sqlite3

from django.conf import settings
from django.core.management import call_command
from django.db import connection
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from conreq.utils.environment import get_database_engine

DB_ENGINE = get_database_engine()
HUEY_FILENAME = getattr(settings, "HUEY_FILENAME")


@db_periodic_task(crontab(minute="0", hour="0", day_of_week="1"))
def clean_background_task_db():
    """Periodically performs a SQLITE vacuum on the background task database weekly."""
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
        """Periodically performs any cleanup tasks needed for the default database weekly."""
        with connection.cursor() as cursor:
            cursor.execute("VACUUM")


@db_periodic_task(crontab(minute="0", hour="0", day="1"))
def clean_sessions():
    """Periodically deletes expired sessions from the database monthly."""
    call_command("clearsessions")
