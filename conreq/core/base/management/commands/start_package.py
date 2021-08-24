from django.conf import settings
from django.core.management import call_command
from django.core.management.templates import TemplateCommand

PACKAGES_DIR = getattr(settings, "PACKAGES_DEV_DIR")
PACKAGE_TEMPLATE = getattr(settings, "PACKAGE_TEMPLATE")
PACKAGE_SLIM_TEMPLATE = getattr(settings, "PACKAGE_SLIM_TEMPLATE")


class Command(TemplateCommand):
    help = "Creates a Conreq package structure with given name."

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
        # parser.add_argument(
        #     "--slim",
        #     action="store_true",
        #     help="Creates the bare minimum structure required.",
        # )
