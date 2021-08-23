import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

APPS_DIR = getattr(settings, "APPS_DIR")
BASE_DIR = getattr(settings, "BASE_DIR")
APP_TEMPLATE_DIR = os.path.join(BASE_DIR, "conreq", "app_template")


class Command(BaseCommand):
    help = "Creates all files needed to start a new Conreq app."

    def handle(self, *args, **options):
        call_command(
            "startapp",
            "--template=" + APP_TEMPLATE_DIR,
            options["name"],
            APPS_DIR,
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "name",
            help="Name of the new app.",
        )
