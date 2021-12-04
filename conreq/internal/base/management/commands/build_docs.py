from subprocess import run

from django.conf import settings
from django.core.management.base import BaseCommand

DOCS_DIR = getattr(settings, "ROOT_DIR") / "docs"


class Command(BaseCommand):
    help = "Builds the docs using MkDocs."

    def handle(self, *args, **options):
        run(
            ["mkdocs", "build", "-d", DOCS_DIR / "deploy"],
            cwd=DOCS_DIR / "source",
            check=True,
        )
