from logging.config import dictConfig as logging_config
from multiprocessing import Process

import django
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import BaseCommand
from huey.contrib.djhuey import db_task
from hypercorn.config import Config as HypercornConfig
from hypercorn.run import run as run_hypercorn

from conreq.utils.database import backup, backup_needed
from conreq.utils.environment import get_debug

HYPERCORN_TOML = getattr(settings, "DATA_DIR") / "hypercorn.toml"
DEBUG = get_debug()
HUEY_FILENAME = getattr(settings, "HUEY_FILENAME")
ACCESS_LOG_FILE = getattr(settings, "ACCESS_LOG_FILE")


class Command(BaseCommand):
    help = "Runs all commands needed to safely start Conreq."

    def handle(self, *args, **options):
        port = options["port"]
        verbosity = "-v 1" if DEBUG else "-v 0"

        # Run any preconfiguration tasks
        if not options["disable_preconfig"]:
            preconfig_args = [
                "preconfig_conreq",
                options["uid"],
                options["gid"],
            ]
            if not options["set_perms"]:
                preconfig_args.append("--no-perms")
            call_command(*preconfig_args, verbosity)

        # Execute tests to ensure Conreq is healthy before starting
        if not options["skip_checks"]:
            call_command("check")
        if options["test"]:
            call_command("test", "--noinput", "--parallel", "--failfast")

        # Queue a task to backup the database if needed
        backup_db()

        # Perform any debug related clean-up
        if DEBUG:
            print("Conreq is in DEBUG mode.")
            print("Clearing cache...")
            cache.clear()

        # Migrate the database
        call_command("migrate", "--noinput", verbosity)

        if not DEBUG:
            # Collect static files
            call_command("collectstatic", "--link", "--clear", "--noinput", verbosity)
            call_command("compress", "--force", verbosity)

        # Run background task management
        proc = Process(target=self.start_huey, daemon=True)
        proc.start()

        # Run the production webserver
        if not DEBUG:
            self._run_webserver(port)

        # Run the development webserver
        if DEBUG:
            call_command("runserver", f"0.0.0.0:{port}")

    @staticmethod
    def _run_webserver(port):
        # TODO: Switch to Uvicorn when this is resolved
        # https://github.com/encode/uvicorn/issues/342
        hypercorn_config = HypercornConfig()
        hypercorn_config.bind = f"0.0.0.0:{port}"
        hypercorn_config.websocket_ping_interval = 20
        hypercorn_config.workers = settings.WEBSERVER_WORKERS
        hypercorn_config.application_path = "conreq.asgi:application"
        hypercorn_config.accesslog = ACCESS_LOG_FILE

        # Additonal webserver configuration
        if HYPERCORN_TOML.exists():
            hypercorn_config.from_toml(HYPERCORN_TOML)

        # Run the webserver
        run_hypercorn(hypercorn_config)

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
        parser.add_argument(
            "--set-perms",
            action="store_true",
            help="Have Conreq set permissions during preconfig.",
        )
        parser.add_argument(
            "--test",
            action="store_true",
            help="Run tests before starting Conreq.",
        )

    @staticmethod
    def start_huey():
        """Starts the Huey background task manager."""
        logging_initial = getattr(settings, "LOGGING_INITIAL")
        logging_config(logging_initial)
        django.setup()
        if DEBUG:
            call_command("run_huey")
        else:
            call_command("run_huey", "--quiet")


@db_task()
def backup_db():
    """Performs a backup if the last backup was longer than the threshold."""
    if backup_needed():
        backup()
