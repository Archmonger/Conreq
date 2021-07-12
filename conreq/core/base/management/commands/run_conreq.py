import os
from multiprocessing import Process
import sqlite3

import django
from conreq.utils.generic import get_debug_from_env
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import BaseCommand
from hypercorn.config import Config as HypercornConfig
from hypercorn.run import run as run_hypercorn

HYPERCORN_TOML = os.path.join(getattr(settings, "DATA_DIR"), "hypercorn.toml")
DEBUG = get_debug_from_env()
HUEY_STORAGE = getattr(settings, "HUEY_STORAGE")


class Command(BaseCommand):
    help = "Runs all commands needed to safely start Conreq."

    def handle(self, *args, **options):
        port = options["port"]

        # Run any preconfiguration tasks
        if not options["disable_preconfig"]:
            call_command("preconfig_conreq", options["uid"], options["gid"])

        # Execute tests to ensure Conreq is healthy before starting
        if not options["skip_checks"]:
            call_command("test", "--noinput", "--failfast")

        # Perform any Debug related clean-up
        if DEBUG:
            print("Conreq is in DEBUG mode.")
            print("DEBUG: Clearing cache...")
            cache.clear()
            self.reset_huey_db()
            call_command("makemigrations", "silk")

        # Migrate the database
        call_command("migrate", "--noinput")

        if not DEBUG:
            # Collect static files
            call_command("collectstatic", "--link", "--noinput")
            call_command("compress", "--force")

        # Run background task management
        proc = Process(target=self.start_huey, daemon=True)
        proc.start()

        # Run the production webserver
        if not DEBUG:
            config = HypercornConfig()
            config.bind = f"0.0.0.0:{port}"
            config.websocket_ping_interval = 20
            config.workers = 6
            config.application_path = "conreq.asgi:application"
            config.accesslog = getattr(settings, "ACCESS_LOG_FILE")

            # Additonal webserver configuration
            if os.path.exists(HYPERCORN_TOML):
                config.from_toml(HYPERCORN_TOML)

            # Run the webserver
            run_hypercorn(config)

        # Run the development webserver
        if DEBUG:
            call_command("runserver", f"0.0.0.0:{port}")

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--port",
            help="Select the port number for Conreq to run on.",
            default=8000,
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

    @staticmethod
    def reset_huey_db():
        """Deletes all entries within the Huey background task database."""
        with sqlite3.connect(HUEY_STORAGE) as cursor:
            tables = list(
                cursor.execute("select name from sqlite_master where type is 'table'")
            )
            cursor.executescript(";".join(["delete from %s" % i for i in tables]))
        print("DEBUG: Removing stale background tasks...")

    @staticmethod
    def start_huey():
        """Starts the Huey background task manager."""
        django.setup()
        if DEBUG:
            call_command("run_huey")
        if not DEBUG:
            call_command("run_huey", "--quiet")
