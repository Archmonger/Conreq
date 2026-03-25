from django.db import connection
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from conreq.utils.environment import get_database_type

DB_ENGINE = get_database_type()


if DB_ENGINE == "SQLITE3":

    @db_periodic_task(crontab(minute="0", hour="0", strict=True), expires=120)
    def conreq_db_maintenance():
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA optimize;")
            cursor.execute("VACUUM;")
            cursor.execute("REINDEX;")
