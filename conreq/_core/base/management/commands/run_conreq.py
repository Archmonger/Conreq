import contextlib
import os
import signal
import subprocess
import sys

import uvicorn
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key
from uvicorn.config import LOGGING_CONFIG as UVICORN_LOGGING_CONFIG

from conreq import config
from conreq.utils.backup import backup_needed, backup_now
from conreq.utils.environment import get_debug_mode, get_env, set_env

HUEY_PID_FILE = getattr(settings, "PID_DIR") / "huey.pid"
DEBUG = get_debug_mode()


class Command(BaseCommand):
    help = "Runs all commands needed to safely start Conreq."

    def handle(self, *args, **options):
        # pylint: disable=attribute-defined-outside-init
        self.bind = (
            options["bind"]
            or f"{get_env('HOST_IP', '0.0.0.0')}:{get_env('HOST_PORT', '7575')}"
        )
        self.host = self.bind.split(":")[0]
        self.port = int(self.bind.split(":")[1])
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
        if backup_needed():
            backup_now()

        # Perform any debug related clean-up
        if DEBUG:
            print("Conreq is in DEBUG mode.")
            print("Clearing cache...")
            cache.clear()

        # Migrate the database
        for database in settings.DATABASES.keys():
            call_command(
                "migrate",
                "--database",
                database,
                "--noinput",
                verbosity,
            )

        if not DEBUG:
            # Collect static files
            call_command("collectstatic", "--link", "--clear", "--noinput", verbosity)
            call_command("compress", "--force", verbosity)

        # Rotate the secret key if needed
        if get_env("ROTATE_SECRET_KEY", return_type=bool):
            set_env("WEB_ENCRYPTION_KEY", get_random_secret_key())

        # Run background task management
        # FIXME: This causes some duplicate logging during startup.
        self.stop_huey()
        proc = self.start_huey()
        if proc.pid:
            with open(HUEY_PID_FILE, "w", encoding="utf-8") as huey_pid:
                huey_pid.write(str(proc.pid))

        # Run pre-run functions before starting the webserver
        for script in config.startup.functions:
            script()

        # Run background processes before starting the webserver
        for process in config.startup.processes:
            process.start()

        # Run the webserver
        self._run_webserver()

    def _run_webserver(self):
        # pylint: disable=import-outside-toplevel
        from conreq._core.server_settings.models import WebserverSettings

        # TODO: Add in Uvicorn's reverse proxy stuff
        db_conf: WebserverSettings = WebserverSettings.get_solo()
        config_kwargs = {
            "ssl_certfile": self._f_path(db_conf.ssl_certificate),
            "ssl_keyfile": self._f_path(db_conf.ssl_key),
            "ssl_ca_certs": self._f_path(db_conf.ssl_ca_certificate),
        }

        # Run the webserver
        debug = get_env("WEBSERVER_DEBUG", return_type=bool)
        uvicorn.run(
            "conreq.asgi:application",
            host=self.host,
            port=self.port,
            workers=settings.WEBSERVER_WORKERS,
            log_config=UVICORN_LOGGING_CONFIG if debug else {"version": 1},
            log_level="debug" if debug else None,
            server_header=False,
            **config_kwargs,
        )

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
        start_command = f"{sys.executable} manage.py run_huey"
        return subprocess.Popen(start_command.split(" "))

    @staticmethod
    def stop_huey():
        """Stops the Huey background task manager.
        Required to prevent duplicate Huey instances if using live reloading."""
        if not HUEY_PID_FILE.exists():
            return

        with open(HUEY_PID_FILE, encoding="utf-8") as huey_pid:
            pid = int(huey_pid.read())
            if not pid:
                return
            with contextlib.suppress(OSError):
                os.kill(pid, signal.SIGTERM)

    @staticmethod
    def _f_path(model_obj):
        if model_obj:
            return model_obj.path
