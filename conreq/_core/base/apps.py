from sqlite3 import Connection

from django.apps import AppConfig
from django.db.backends.signals import connection_created
from idom.html import i

from conreq import config
from conreq.types import NavGroup


class BaseConfig(AppConfig):
    name = "conreq._core.base"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from django_idom import IDOM_WEBSOCKET_PATH

        config.asgi.websockets.append(IDOM_WEBSOCKET_PATH)
        config.homepage.nav_tabs.add(
            NavGroup(name="User", icon=i({"className": "fas fa-users icon-left"}))
        )
        config.homepage.nav_tabs.add(
            NavGroup(name="Admin", icon=i({"className": "fas fa-cogs icon-left"}))
        )


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
