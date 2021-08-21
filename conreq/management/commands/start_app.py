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
APP_TEMPLATE = getattr(settings, "APP_TEMPLATE")


class Command(TemplateCommand):
    """Minor rewrite of TemplateCommand to be able to create Conreq subapps."""

    help = (
        "Creates a Conreq sub app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )

    def handle(self, name, subapp_name="main", **options):
        # TODO: Rewrite this (Currently copy-pasta'd from Django's startapp command)
        self.app_or_project = "app"
        self.a_or_an = "an"
        self.paths_to_remove = []
        self.verbosity = options["verbosity"]

        self.validate_name(name)
        target = os.path.join(PACKAGES_DIR, name, subapp_name)

        # if some directory is given, make sure it's nicely expanded
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
                % ("app", ", ".join(extensions))
            )
            self.stdout.write(
                "Rendering %s template files with filenames: %s"
                % ("app", ", ".join(extra_files))
            )
        base_name = "app_name"
        base_subdir = "app_template"
        base_directory = "app_directory"
        camel_case_name = "camel_case_app_name"
        camel_case_value = "".join(x for x in name.title() if x != "_")

        context = Context(
            {
                **options,
                base_name: name,
                base_directory: top_dir,
                camel_case_name: camel_case_value,
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
                        "%s already exists. Overlaying %s app into an existing "
                        "directory won't replace conflicting files."
                        % (
                            new_path,
                            self.a_or_an,
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
        parser.add_argument("app", help="Name of the application or project.")
        parser.add_argument("subapp", help="Name of the sub application.")
        parser.add_argument(
            "--extension",
            "-e",
            dest="extensions",
            action="append",
            default=["py"],
            help='The file extension(s) to render (default: "py"). '
            "Separate multiple extensions with commas, or use "
            "-e multiple times.",
        )
        parser.add_argument(
            "--name",
            "-n",
            dest="files",
            action="append",
            default=[],
            help="The file name(s) to render. Separate multiple file names "
            "with commas, or use -n multiple times.",
        )
        parser.add_argument(
            "--slim",
            action="store_true",
            help="Creates the bare minimum structure required.",
        )
