import os
import shutil
import sqlite3
import sys

from conreq.utils.generic import cprint, get_database_type
from django.conf import settings
from django.core.management.base import BaseCommand

DATA_DIR = getattr(settings, "DATA_DIR")
DATABASES = getattr(settings, "DATABASES")
HUEY_STORAGE = getattr(settings, "HUEY_STORAGE")
CACHES = getattr(settings, "CACHES")
LOG_DIR = getattr(settings, "LOG_DIR")
SILKY_PYTHON_PROFILER_RESULT_PATH = getattr(
    settings, "SILKY_PYTHON_PROFILER_RESULT_PATH"
)


class Command(BaseCommand):
    help = "Runs any tasks that may help with preconfiguration."

    def handle(self, *args, **options):
        uid = options["uid"]
        gid = options["gid"]

        cprint("Preconfiguring Conreq...", "bold")

        # Django database
        if get_database_type() == "SQLITE3":
            database = DATABASES["default"]["NAME"]
            self.setup_sqlite_database(database, "Conreq", uid, gid)

        # Background task database
        if HUEY_STORAGE:
            self.setup_sqlite_database(HUEY_STORAGE, "Background Task", uid, gid)

        if sys.platform == "linux":
            # Cache database
            self.recursive_chown(CACHES["default"]["LOCATION"], uid, gid)

            # Logs folder
            self.recursive_chown(LOG_DIR, uid, gid)

            # Debug dir
            self.recursive_chown(SILKY_PYTHON_PROFILER_RESULT_PATH, uid, gid)

    def add_arguments(self, parser):
        parser.add_argument(
            "uid",
            nargs="?",
            help="User ID to chown to (Linux only). Defaults to the current user. Use -1 to remain unchanged.",
            type=int,
            default=0,
        )
        parser.add_argument(
            "gid",
            nargs="?",
            help="Group ID to chown to (Linux only). Defaults to the current user. Use -1 to remain unchanged.",
            type=int,
            default=0,
        )

    @staticmethod
    def setup_sqlite_database(path, name, uid, gid):
        cprint(name.rstrip(" ") + " Database", "header")
        if not os.path.exists(path):
            cprint("> Creating database", "blue")
        with sqlite3.connect(path) as cursor:
            cprint("> Vacuuming database", "blue")
            cursor.execute("VACUUM")
        if uid != -1 or gid != -1:
            if sys.platform == "linux":
                cprint("> Applying permissions", "blue")
                new_uid = uid if uid else os.getuid()
                new_gid = gid if gid else os.getgid()
                os.chown(path, new_uid, new_gid)
        cprint("> Complete", "blue")

    @staticmethod
    def recursive_chown(path, uid, gid):
        cprint('Recursively applying permissions to "' + path + '"', "header")
        new_uid = uid if uid != -1 else None
        new_gid = gid if gid != -1 else None
        if uid != -1 or gid != -1:
            for dirpath, dirnames, filenames in os.walk(path):
                shutil.chown(dirpath, new_uid, new_gid)
                for filename in filenames:
                    shutil.chown(os.path.join(dirpath, filename), new_uid, new_gid)
