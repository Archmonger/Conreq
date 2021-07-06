import os
from multiprocessing import Process

import django
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from hypercorn.config import Config as HypercornConfig
from hypercorn.run import run as run_hypercorn

HYPERCORN_TOML = os.path.join(getattr(settings, "DATA_DIR"), "hypercorn.toml")


class Command(BaseCommand):
    help = "Runs all commands needed to safely start Conreq."

    @staticmethod
    def start_huey():
        django.setup()
        call_command("run_huey", "--quiet")

    def handle(self, *args, **options):
        # Run any preparation steps
        call_command("migrate", "--noinput")
        call_command("collectstatic", "--link", "--noinput")
        call_command("compress", "--force")

        # Run background task management
        p = Process(target=self.start_huey, daemon=True)
        p.start()

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
