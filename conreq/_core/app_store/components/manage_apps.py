import importlib
import subprocess
import threading

import pkg_resources as pkg
from reactpy import component, hooks, html
from reactpy_django.components import django_css

from conreq.utils.environment import get_env


@component
def manage_apps():
    """Bootstrap table for managing apps.
    Apps contain the following action buttons: logs, upgrade, reinstall, remove, and details
    """

    installed_packages = get_env("INSTALLED_PACKAGES", [], return_type=list)

    return html.div(
        {"class_name": "manage-apps"},
        django_css("conreq/manage_apps.css"),
        django_css("conreq/app_store_card.css"),
        django_css("conreq/table.css"),
        html.table(
            {"class_name": "table table-striped table-hover"},
            html.thead(
                html.tr(
                    html.th("Name"),
                    html.th("Version"),
                    html.th("Status"),
                    html.th("Actions"),
                )
            ),
            html.tbody(*[app_row(app) for app in installed_packages]),
        ),
    )


@component
def app_row(pkg_name: str):
    status, set_status = hooks.use_state("Checking...")
    latest_version, set_latest_version = hooks.use_state("")
    metadata_dir = getattr(pkg.get_distribution(pkg_name), "egg_info")
    module_name = (
        open(f"{metadata_dir}/top_level.txt", encoding="UTF-8").read().rstrip()
    )
    module = importlib.import_module(module_name)

    @hooks.use_effect(dependencies=[])
    async def get_status():
        def thread_func():
            """Runs `pip index versions {app.pkg_name}` and parses the latest version."""
            proc = subprocess.Popen(
                ["pip", "index", "versions", pkg_name, "--no-input"],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if not proc.stdout:
                set_status("Error while checking for updates")
                return
            lines = proc.stdout.readlines()
            for line in lines:
                if line.strip().startswith(b"LATEST:"):
                    version = line.split(b":")[1].strip().decode()
                    set_latest_version(version)
                    if version == module.__version__:
                        set_status("Up to date")
                    else:
                        set_status(f"Update available ({version})")

        threading.Thread(target=thread_func, daemon=True).start()

    return html.tr(
        html.td(pkg_name),
        html.td(module.__version__),
        html.td(status),
        html.td(html.div("Actions")),
    )
