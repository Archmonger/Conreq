from logging.config import dictConfig as logging_config
from multiprocessing import Process

import django
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key
from huey.contrib.djhuey import db_task
from hypercorn.config import Config as HypercornConfig
from hypercorn.run import run as run_hypercorn

from conreq.utils.backup import backup_needed, backup_now
from conreq.utils.environment import get_debug_mode, get_env, set_env

HYPERCORN_TOML = getattr(settings, "DATA_DIR") / "hypercorn.toml"
DEBUG = get_debug_mode()


class Command(BaseCommand):
    help = "Runs all commands needed to safely start Conreq."

    def handle(self, *args, **options):
        host = get_env("WEBSERVER_HOST", "0.0.0.0")
        port = get_env("WEBSERVER_PORT", "7575")
        bind = options["bind"] or f"{host}:{port}"
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
        backup_if_needed()

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

        # Rotate the secret key if needed
        if get_env("ROTATE_SECRET_KEY", return_type=bool):
            set_env("WEB_ENCRYPTION_KEY", get_random_secret_key())

        # Run background task management
        proc = Process(target=self.start_huey, daemon=True)
        proc.start()

        # Run the production webserver
        if not DEBUG:
            self._run_webserver(bind)

        # Run the development webserver
        if DEBUG:
            call_command("runserver", bind)

    @staticmethod
    def _run_webserver(bind):
        # pylint: disable=import-outside-toplevel, invalid-name
        from conreq._core.server_settings.models import WebserverSettings

        # TODO: Switch to Uvicorn when this is resolved
        # https://github.com/encode/uvicorn/issues/342
        config = HypercornConfig()
        config.bind = bind
        config.websocket_ping_interval = 20
        config.workers = settings.WEBSERVER_WORKERS
        config.application_path = "conreq.asgi:application"
        config.accesslog = settings.ACCESS_LOG_FILE
        config.debug = get_env("WEBSERVER_DEBUG", return_type=bool)
        config.include_server_header = False
        x: WebserverSettings = WebserverSettings.get_solo()
        if x.ssl_certificate and x.ssl_key:
            config.certfile = x.ssl_certificate.path
            config.keyfile = x.ssl_key.path
            if x.ssl_ca_certificate:
                config.ca_certs = x.ssl_ca_certificate.path

        # Additonal webserver configuration
        if HYPERCORN_TOML.exists():
            config.from_toml(HYPERCORN_TOML)

        # Run the webserver
        run_hypercorn(config)

    def add_arguments(self, parser):
        parser.add_argument(
            "-b",
            "--bind",
            help="Set the 'host_address:port' for Conreq to run on.",
            default="0.0.0.0:7575",
            type=str,
        )
        parser.add_argument(
            "--disable-preconfig",
            action="store_true",
            help="Disables Conreq's preconfiguration prior to startup.",
        )
        parser.add_argument(
            "--uid",
            help="User ID for files and sockets (Linux only). Defaults to the current user. Use -1 to remain unchanged.",
            type=int,
            default=0,
        )
        parser.add_argument(
            "--gid",
            help="Group ID for files and sockets (Linux only). Defaults to the current user. Use -1 to remain unchanged.",
            type=int,
            default=0,
        )
        parser.add_argument(
            "--set-perms",
            action="store_true",
            help="Have Conreq set file permissions during preconfig.",
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
def backup_if_needed():
    """Performs a backup if the last backup was longer than the threshold."""
    if backup_needed():
        backup_now()
