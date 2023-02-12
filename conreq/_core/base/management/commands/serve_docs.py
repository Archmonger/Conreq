from subprocess import run

from django.conf import settings
from django.core.management.base import BaseCommand

DOCS_SOURCE_DIR = getattr(settings, "ROOT_DIR") / "docs" / "source"


class Command(BaseCommand):
    help = "Starts up the MkDocs preview webserver."

    def handle(self, *args, **options):
        run(["mkdocs", "serve"], cwd=DOCS_SOURCE_DIR, check=True)
