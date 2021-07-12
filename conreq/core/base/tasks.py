import sqlite3

from conreq.utils.generic import get_database_type
from django.conf import settings
from django.db import connection
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

DB_ENGINE = get_database_type()
HUEY_STORAGE = getattr(settings, "HUEY_STORAGE")


@db_periodic_task(crontab(minute="0", hour="12", day="1/1"))
def bg_tasks_vacuum():
    """Periodically preforms a SQLITE vacuum on the background task database."""
    with sqlite3.connect(HUEY_STORAGE) as cursor:
        cursor.execute("VACUUM")


@db_periodic_task(crontab(minute="0", hour="12", day="1/1"))
def db_vacuum():
    """Periodically performs any cleanup tasks needed for the default database."""
    if DB_ENGINE == "SQLITE3":
        with connection.cursor() as cursor:
            cursor.execute("VACUUM")
