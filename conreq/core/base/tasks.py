import os
import sqlite3

from conreq.core.arrs.sonarr_radarr import ArrManager
from conreq.settings import HUEY_STORAGE
from conreq.utils.generic import get_database_type
from django.db import connection
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

ARR_REFRESH_INTERNAL = os.environ.get("ARR_REFRESH_INTERNAL", "*/1")
DB_ENGINE = get_database_type()


@db_periodic_task(crontab(minute=ARR_REFRESH_INTERNAL))
def refresh_content():
    """Checks Sonarr/Radarr for new entries every minute."""
    ArrManager().refresh_content()


@db_task()
def background_task(function, *args, **kwargs):
    """Adds any function to the background task queue."""
    function(*args, **kwargs)


@db_periodic_task(crontab(minute="0", hour="12", day="1/1"))
def bg_tasks_vacuum():
    """Periodically preforms a SQLITE vacuum on the background task database."""
    with sqlite3.connect(HUEY_STORAGE) as conn:
        conn.execute("VACUUM")


@db_periodic_task(crontab(minute="0", hour="12", day="1/1"))
def db_vacuum():
    """Periodically performs any cleanup tasks needed for the default database."""
    if DB_ENGINE == "SQLITE3":
        with connection.cursor() as cursor:
            cursor.execute("VACUUM")
