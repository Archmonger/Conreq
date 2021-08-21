from django.conf import settings
from django.core.management import call_command
from django.core.management.templates import TemplateCommand

PACKAGES_DIR = getattr(settings, "PACKAGES_DIR")
PACKAGE_TEMPLATE = getattr(settings, "PACKAGE_TEMPLATE")


class Command(TemplateCommand):
    help = (
        "Creates a Conreq app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )

    def handle(self, *args, **options):
        call_command(
            "startapp",
            "--template=" + PACKAGE_TEMPLATE,
            options["package_name"],
            PACKAGES_DIR,
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "package_name",
            help="Name of the new app.",
        )
        parser.add_argument(
            "--slim",
            action="store_true",
            help="Creates the bare minimum structure required.",
        )
