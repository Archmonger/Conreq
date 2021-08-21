import os
import shutil

import django
from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand
from django.core.management.utils import handle_extensions
from django.template import Context, Engine
from django.utils.version import get_docs_version

PACKAGES_DIR = getattr(settings, "PACKAGES_DIR")
PACKAGE_TEMPLATE = getattr(settings, "PACKAGE_TEMPLATE")
APP_TEMPLATE = getattr(settings, "APP_TEMPLATE")


class Command(TemplateCommand):
    """Minor rewrite of TemplateCommand to be able to create Conreq subapps."""

    help = (
        "Creates a Conreq app directory structure for the given package in "
        "the current directory or optionally in the given directory."
    )

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

        # pylint: disable=attribute-defined-outside-init,raise-missing-from
        # TemplateCommand.handle() source code starts here
        self.app_or_project = app_or_project
        self.a_or_an = "an" if app_or_project == "app" else "a"
        self.paths_to_remove = []
        self.verbosity = options["verbosity"]

        self.validate_name(name)

        # if some directory is given, make sure it's nicely expanded
        if target is None:
            top_dir = os.path.join(os.getcwd(), name)
            try:
                os.makedirs(top_dir)
            except FileExistsError:
                raise CommandError("'%s' already exists" % top_dir)
            except OSError as e:
                raise CommandError(e)
        else:
            if app_or_project == "app":
                self.validate_name(os.path.basename(target), "directory")
            top_dir = os.path.abspath(os.path.expanduser(target))
            if not os.path.exists(top_dir):
                raise CommandError(
                    "Destination directory '%s' does not "
                    "exist, please create it first." % top_dir
                )

        extensions = tuple(handle_extensions(options["extensions"]))
        extra_files = []
        for file in options["files"]:
            extra_files.extend(map(lambda x: x.strip(), file.split(",")))
        if self.verbosity >= 2:
            self.stdout.write(
                "Rendering %s template files with extensions: %s"
                % (app_or_project, ", ".join(extensions))
            )
            self.stdout.write(
                "Rendering %s template files with filenames: %s"
                % (app_or_project, ", ".join(extra_files))
            )
        base_name = "%s_name" % app_or_project
        base_subdir = "%s_template" % app_or_project
        base_directory = "%s_directory" % app_or_project
        camel_case_name = "camel_case_%s_name" % app_or_project
        camel_case_value = "".join(x for x in name.title() if x != "_")

        context = Context(
            {
                **options,
                base_name: name,
                base_directory: top_dir,
                camel_case_name: camel_case_value,
                "package_name": package_name,
                "docs_version": get_docs_version(),
                "django_version": django.__version__,
            },
            autoescape=False,
        )

        # Setup a stub settings environment for template rendering
        if not settings.configured:
            settings.configure()
            django.setup()

        template_dir = self.handle_template(options["template"], base_subdir)
        prefix_length = len(template_dir) + 1

        for root, dirs, files in os.walk(template_dir):

            path_rest = root[prefix_length:]
            relative_dir = path_rest.replace(base_name, name)
            if relative_dir:
                target_dir = os.path.join(top_dir, relative_dir)
                os.makedirs(target_dir, exist_ok=True)

            for dirname in dirs[:]:
                if dirname.startswith(".") or dirname == "__pycache__":
                    dirs.remove(dirname)

            for filename in files:
                if filename.endswith((".pyo", ".pyc", ".py.class")):
                    # Ignore some files as they cause various breakages.
                    continue
                old_path = os.path.join(root, filename)
                new_path = os.path.join(
                    top_dir, relative_dir, filename.replace(base_name, name)
                )
                for old_suffix, new_suffix in self.rewrite_template_suffixes:
                    if new_path.endswith(old_suffix):
                        new_path = new_path[: -len(old_suffix)] + new_suffix
                        break  # Only rewrite once

                if os.path.exists(new_path):
                    raise CommandError(
                        "%s already exists. Overlaying %s %s into an existing "
                        "directory won't replace conflicting files."
                        % (
                            new_path,
                            self.a_or_an,
                            app_or_project,
                        )
                    )

                # Only render the Python files, as we don't want to
                # accidentally render Django templates files
                if new_path.endswith(extensions) or filename in extra_files:
                    with open(old_path, encoding="utf-8") as template_file:
                        content = template_file.read()
                    template = Engine().from_string(content)
                    content = template.render(context)
                    with open(new_path, "w", encoding="utf-8") as new_file:
                        new_file.write(content)
                else:
                    shutil.copyfile(old_path, new_path)

                if self.verbosity >= 2:
                    self.stdout.write("Creating %s" % new_path)
                try:
                    shutil.copymode(old_path, new_path)
                    self.make_writeable(new_path)
                except OSError:
                    self.stderr.write(
                        "Notice: Couldn't set permission bits on %s. You're "
                        "probably using an uncommon filesystem setup. No "
                        "problem." % new_path,
                        self.style.NOTICE,
                    )

        if self.paths_to_remove:
            if self.verbosity >= 2:
                self.stdout.write("Cleaning up temporary files.")
            for path_to_remove in self.paths_to_remove:
                if os.path.isfile(path_to_remove):
                    os.remove(path_to_remove)
                else:
                    shutil.rmtree(path_to_remove)

    def add_arguments(self, parser):
        parser.add_argument("package_name", help="Name of the application or project.")
        parser.add_argument("app_name", help="Name of the sub application.")
        parser.add_argument(
            "--slim",
            action="store_true",
            help="Creates the bare minimum structure required.",
        )
