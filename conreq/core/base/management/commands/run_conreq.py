import contextlib
import os
from logging import getLogger
from multiprocessing import Process
from time import sleep

import django
import uvicorn
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import BaseCommand

from conreq.utils.environment import get_debug

UVICORN_CONFIG = os.path.join(getattr(settings, "DATA_DIR"), "uvicorn.env")
DEBUG = get_debug()
HUEY_FILENAME = getattr(settings, "HUEY_FILENAME")
ACCESS_LOG_FILE = getattr(settings, "ACCESS_LOG_FILE")

_logger = getLogger(__name__)


class Command(BaseCommand):
    help = "Runs all commands needed to safely start Conreq."

    def handle(self, *args, **options):
        port = options["port"]
        verbosity = "-v 1" if DEBUG else "-v 0"

        # Perform clean-up
        print("Removing stale background tasks...")
        self.reset_huey_db()
        if DEBUG:
            print("Clearing cache...")
            cache.clear()

        # Run any preconfiguration tasks
        if not options["disable_preconfig"]:
            preconfig_args = [
                "preconfig_conreq",
                options["uid"],
                options["gid"],
            ]
            if not options["set_perms"]:
                preconfig_args.append("--no-perms")
            call_command(*preconfig_args)

        # Execute tests to ensure Conreq is healthy before starting
        if not options["skip_checks"]:
            call_command("test", "--noinput", "--parallel", "--failfast")

        # Migrate the database
        call_command("migrate", "--noinput", verbosity)

        # Collect static files
        if not DEBUG:
            call_command("collectstatic", "--link", "--clear", "--noinput", verbosity)
            call_command("compress", "--force", verbosity)

        huey = Process(target=start_huey)
        huey.start()
        webserver = Process(target=start_webserver, kwargs={"port": port})
        webserver.start()

        while True:
            if not huey.is_alive():
                _logger.warning("Background task manager has crashed. Restarting...")
                huey = Process(target=start_huey, daemon=True)
                huey.start()

            if not webserver.is_alive():
                _logger.warning("Webserver has crashed. Restarting...")
                webserver = Process(target=start_webserver, kwargs={"port": port})
                webserver.start()

            sleep(5)

    @staticmethod
    def reset_huey_db():
        """Deletes the huey database"""
        with contextlib.suppress(Exception):
            if os.path.exists(HUEY_FILENAME):
                os.remove(HUEY_FILENAME)
        with contextlib.suppress(Exception):
            if os.path.exists(f"{HUEY_FILENAME}-shm"):
                os.remove(f"{HUEY_FILENAME}-shm")
        with contextlib.suppress(Exception):
            if os.path.exists(f"{HUEY_FILENAME}-wal"):
                os.remove(f"{HUEY_FILENAME}-wal")

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--port",
            help="Select the port number for Conreq to run on.",
            default=7575,
            type=int,
        )

        parser.add_argument(
            "--disable-preconfig",
            action="store_true",
            help="Disables Conreq's preconfiguration prior to startup.",
        )

        parser.add_argument(
            "--uid",
            help="User ID to chown to (Linux only). Defaults to the current user. Use -1 to remain unchanged.",
            type=int,
            default=0,
        )

        parser.add_argument(
            "--gid",
            help="Group ID to chown to (Linux only). Defaults to the current user. Use -1 to remain unchanged.",
            type=int,
            default=0,
        )

        parser.add_argument(
            "--set-perms",
            action="store_true",
            help="Have Conreq set permissions during preconfig.",
        )


def start_webserver(port):
    django.setup()

    uvicorn.run(
        "conreq.asgi:application",
        host="0.0.0.0",
        port=port,
        ws_ping_interval=10,
        workers=1 if DEBUG else (os.cpu_count() or 8),
        access_log=ACCESS_LOG_FILE,
        reload=DEBUG,
        env_file=UVICORN_CONFIG if os.path.exists(UVICORN_CONFIG) else None,
    )


def start_huey():
    """Starts the Huey background task manager."""
    django.setup()
    print("Starting Huey background task manager...")

    if DEBUG:
        call_command("run_huey")
    else:
        call_command("run_huey", "--quiet")
