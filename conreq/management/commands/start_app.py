import os

from django.conf import settings
from django.core.management.templates import TemplateCommand

PACKAGES_DIR = getattr(settings, "PACKAGES_DIR")
PACKAGE_TEMPLATE = getattr(settings, "PACKAGE_TEMPLATE")
APP_TEMPLATE = getattr(settings, "APP_TEMPLATE")
APP_SLIM_TEMPLATE = getattr(settings, "APP_SLIM_TEMPLATE")


class Command(TemplateCommand):
    help = "Creates a Conreq app structure within a package."

    # pylint: disable=arguments-differ
    def handle(self, package_name, app_name, **options):
        # Conreq Customizatizations to TemplateCommand.handle()
        name = app_name
        app_or_project = "app"
        target = os.path.join(PACKAGES_DIR, package_name, "apps")
        options["template"] = APP_TEMPLATE
        options["extensions"] = ["py"]
        options["files"] = []
        options["template"] = APP_TEMPLATE
        options["package_name"] = package_name
        super().handle(app_or_project, name, target, **options)

    def add_arguments(self, parser):
        parser.add_argument("package_name", help="Name of the application or project.")
        parser.add_argument("app_name", help="Name of the sub application.")
        # parser.add_argument(
        #     "--slim",
        #     action="store_true",
        #     help="Creates the bare minimum structure required.",
        # )
