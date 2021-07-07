import os
from multiprocessing import Process

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


class Command(BaseCommand):
    help = "Runs all commands needed to safely start Conreq."

    @staticmethod
    def start_huey():
        django.setup()
        if DEBUG:
            call_command("run_huey")
        if not DEBUG:
            call_command("run_huey", "--quiet")

    def handle(self, *args, **options):
        if DEBUG:
            print("Conreq is in DEBUG mode. Clearing cache...")
            cache.clear()

        if not DEBUG:
            # Run any preparation steps
            call_command("migrate", "--noinput")
            call_command("collectstatic", "--link", "--noinput")
            call_command("compress", "--force")

        # Run background task management
        proc = Process(target=self.start_huey, daemon=True)
        proc.start()

        if not DEBUG:
            # Default webserver configuration
            config = HypercornConfig()
            config.bind = "0.0.0.0:8000"
            config.websocket_ping_interval = 20
            config.workers = 6
            config.application_path = "conreq.asgi:application"
            config.accesslog = getattr(settings, "ACCESS_LOG_FILE")

            # Additonal webserver configuration
            if os.path.exists(HYPERCORN_TOML):
                config.from_toml(HYPERCORN_TOML)

            # Run the webserver
            run_hypercorn(config)

        if DEBUG:
            # Development webserver
            call_command("runserver", "0.0.0.0:8000")
