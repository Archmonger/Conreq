import sqlite3

from django.conf import settings
from django.db import connection
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from conreq.utils.environment import get_database_type

DB_ENGINE = get_database_type()
HUEY_FILENAME = getattr(settings, "HUEY_FILENAME")


@db_periodic_task(crontab(minute="0", hour="0", strict=True), expires=120)
def huey_db_maintenance():
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
        cursor.execute("PRAGMA optimize;")
        cursor.execute("VACUUM;")
        cursor.execute("REINDEX;")


if DB_ENGINE == "SQLITE3":

    @db_periodic_task(crontab(minute="0", hour="0", strict=True), expires=120)
    def conreq_db_maintenance():
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA optimize;")
            cursor.execute("VACUUM;")
            cursor.execute("REINDEX;")
