import os
import sqlite3

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from conreq.utils.environment import get_database_type, get_debug

DEBUG = get_debug()
BASE_DIR = getattr(settings, "BASE_DIR")
DATA_DIR = getattr(settings, "DATA_DIR")
DATABASES = getattr(settings, "DATABASES")
HUEY_FILENAME = getattr(settings, "HUEY_FILENAME")


class Command(BaseCommand):
    """Executes functions that may require admin privileges,
    since it is expected that run_conreq is executed as a user."""

    help = "Runs code that may be required prior to run_conreq Conreq."

    def handle(self, *args, **options):
        print("Preconfiguring Conreq...")

        # Django database
        if get_database_type() == "SQLITE3":
            database = DATABASES["default"]["NAME"]
            self.setup_sqlite_database(database, "Conreq")

        # Background task database
        if HUEY_FILENAME:
            self.setup_sqlite_database(HUEY_FILENAME, "Background Task")

        if DEBUG:
            # Migrate silk due to their wonky dev choices
            call_command("makemigrations", "silk")

    @staticmethod
    def setup_sqlite_database(path, name):
        if not os.path.exists(path):
            print(f"Creating {name} database")
        with sqlite3.connect(path) as cursor:
            print(f"Optimizing {name} database")
            cursor.execute("PRAGMA optimize;")
            print(f"Vacuuming {name} database")
            cursor.execute("VACUUM;")
            print(f"Reindexing {name} database")
            cursor.execute("REINDEX;")
