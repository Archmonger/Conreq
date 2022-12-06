from django.conf import settings
from django.core.management.templates import TemplateCommand

PACKAGES_DIR = getattr(settings, "PACKAGES_DEV_DIR")
APP_TEMPLATE = getattr(settings, "APP_TEMPLATE")
APP_SLIM_TEMPLATE = getattr(settings, "APP_SLIM_TEMPLATE")


class Command(TemplateCommand):
    help = "Creates a Conreq app structure within a package."

    # pylint: disable=arguments-differ
    def handle(self, app_name: str, **options):  # type: ignore
        package_name = options.get("package") or input(
            "Name of the package this app will belong to: "
        ).replace(" ", "_")

        name = app_name
        app_or_project = "app"
        target = str(PACKAGES_DIR / package_name / "apps" / "")
        options["template"] = str(
            APP_SLIM_TEMPLATE if options.get("slim") else APP_TEMPLATE
        )
        options["extensions"] = ["py"]
        options["files"] = []
        options["package_name"] = package_name
        options["verbose_name"] = app_name.replace("_", " ").title()
        super().handle(app_or_project, name, target, **options)

    def add_arguments(self, parser):
        parser.add_argument("app_name", help="Name of the sub application.")
        parser.add_argument(
            "-p", "--package", help="Name of the application or project."
        )
        parser.add_argument(
            "--slim",
            action="store_true",
            help="Creates the bare minimum structure required.",
        )
