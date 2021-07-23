import os
import shutil
import sqlite3
import sys

from conreq.utils.generic import cprint, get_database_type, get_debug_from_env
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

DEBUG = get_debug_from_env()
BASE_DIR = getattr(settings, "BASE_DIR")
DATA_DIR = getattr(settings, "DATA_DIR")
APPS_DIR = getattr(settings, "APPS_DIR")
MEDIA_DIR = getattr(settings, "MEDIA_DIR")
DATABASES = getattr(settings, "DATABASES")
HUEY_FILENAME = getattr(settings, "HUEY_FILENAME")
USER_STATICFILES = getattr(settings, "USER_STATICFILES")
SILKY_PYTHON_PROFILER_RESULT_PATH = getattr(
    settings, "SILKY_PYTHON_PROFILER_RESULT_PATH"
)


class Command(BaseCommand):
    """Executes functions that may require admin privileges,
    since it is expected that run_conreq is executed as a user."""

    help = "Runs code that may be required prior to run_conreq Conreq."

    def handle(self, *args, **options):
        uid = options["uid"]
        gid = options["gid"]
        no_perms = options["no_perms"]

        cprint("Preconfiguring Conreq...", "bold")

        # Django database
        if get_database_type() == "SQLITE3":
            database = DATABASES["default"]["NAME"]
            self.setup_sqlite_database(database, "Conreq", uid, gid, no_perms)

        # Background task database
        if HUEY_FILENAME:
            self.setup_sqlite_database(
                HUEY_FILENAME, "Background Task", uid, gid, no_perms
            )

        # Apps dir
        if not os.path.exists(APPS_DIR):
            os.makedirs(APPS_DIR)

        # User staticfiles dir
        if not os.path.exists(USER_STATICFILES):
            os.makedirs(USER_STATICFILES)

        # User staticfiles dir
        if not os.path.exists(MEDIA_DIR):
            os.makedirs(MEDIA_DIR)

        if DEBUG:
            # Make Silky performance profiling dir
            if not os.path.exists(SILKY_PYTHON_PROFILER_RESULT_PATH):
                os.makedirs(SILKY_PYTHON_PROFILER_RESULT_PATH)

            # Migrate silk due to their wonky dev choices
            call_command("makemigrations", "silk")

        if not no_perms and sys.platform == "linux":
            # Conreq data dir
            self.recursive_chown(DATA_DIR, uid, gid)

            # Conreq core dir
            self.recursive_chown(BASE_DIR, uid, gid)

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

        parser.add_argument(
            "--no-perms",
            action="store_true",
            help="Prevent Conreq from setting permissions.",
        )

    @staticmethod
    def setup_sqlite_database(path, name, uid, gid, no_perms):
        cprint(name.rstrip(" ") + " Database", "header")
        if not os.path.exists(path):
            cprint("> Creating database", "blue")
        with sqlite3.connect(path) as cursor:
            cprint("> Vacuuming database", "blue")
            cursor.execute("VACUUM")
        if not no_perms and (uid != -1 or gid != -1):
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
