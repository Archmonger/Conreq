from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.templates import TemplateCommand

PACKAGES_DIR: Path = getattr(settings, "PACKAGES_DEV_DIR")
PACKAGE_TEMPLATE: Path = getattr(settings, "PACKAGE_TEMPLATE")
PACKAGE_SLIM_TEMPLATE: Path = getattr(settings, "PACKAGE_SLIM_TEMPLATE")


class Command(TemplateCommand):
    help = "Creates a Conreq package structure with given name."

    # pylint: disable=arguments-differ
    def handle(self, package_name: str, **options: dict[str, Any]):  # type: ignore
        name = package_name
        app_or_project = "app"
        target = str(PACKAGES_DIR / "")
        options["template"] = str(
            PACKAGE_SLIM_TEMPLATE if options.get("slim") else PACKAGE_TEMPLATE
        )  # type: ignore
        options["extensions"] = ["py", "txt"]  # type: ignore
        options["files"] = []  # type: ignore
        options["package_name"] = package_name  # type: ignore
        options["verbose_name"] = package_name.replace("_", " ").title()  # type: ignore
        super().handle(app_or_project, name, target, **options)

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
