from sqlite3 import Connection

from django.apps import AppConfig
from django.db.backends.signals import connection_created


class BaseConfig(AppConfig):
    name = "conreq.core.base"


# pylint: disable=unused-argument
@connection_created.connect
def sqlite_connect(sender, connection: Connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == "sqlite":
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode = WAL;")
        cursor.execute("PRAGMA synchronous = NORMAL;")
        cursor.execute("PRAGMA temp_store = MEMORY;")
        cursor.execute("PRAGMA foreign_keys = ON;")


@connection_created.disconnect
def sqlite_disconnect(sender, connection: Connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == "sqlite":
        cursor = connection.cursor()
        cursor.execute("PRAGMA analysis_limit = 400;")
        cursor.execute("PRAGMA optimize;")
