import subprocess
import threading
from logging import getLogger

from reactpy import component, hooks, html
from reactpy_django.components import django_css

from conreq.utils.environment import get_env

_logger = getLogger(__name__)


@component
def manage_apps():
    """Bootstrap table for managing apps.
    Apps contain the following action buttons: logs, upgrade, reinstall, remove, and details
    """

    installed_packages = sorted(
        set(get_env("INSTALLED_PACKAGES", [], return_type=list))
    )

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
                    html.th("Installed"),
                    html.th("Latest"),
                    html.th({"style": {"text-align": "center"}}, "Actions"),
                )
            ),
            html.tbody([app_row(app, key=app) for app in installed_packages]),
        ),
    )


@component
def app_row(pkg_name: str):
    error_msg, set_error_msg = hooks.use_state("")
    current_version, set_current_version = hooks.use_state("")
    latest_version, set_latest_version = hooks.use_state("")

    @hooks.use_effect(dependencies=[])
    async def get_status():
        def thread_func():
            """Runs `pip index versions {app.pkg_name}` and parses the latest version."""
            proc = subprocess.Popen(
                [
                    "pip",
                    "index",
                    "versions",
                    pkg_name,
                    "--no-input",
                ],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            proc.wait()

            # Check if output is broken
            if not proc.stderr or not proc.stdout:
                set_error_msg("Error. Check logs.")
                _logger.error(
                    "Broken stderr or stdout while getting pip index versions for %s",
                    pkg_name,
                )
                return

            # Check if pip index versions failed
            stderr = proc.stderr.readlines()
            for line in stderr:
                if line.strip().startswith(b"ERROR:"):
                    set_error_msg("Error. Check logs.")
                    _logger.error(
                        "'pip index versions' failed for %s: %s",
                        pkg_name,
                        line.strip().decode()[7:],
                    )
                    return

            # Parse output
            stdout = proc.stdout.readlines()
            installed: str = ""
            latest: str = ""
            for line in stdout:
                if line.strip().startswith(b"INSTALLED:"):
                    installed = line.split(b":")[1].strip().decode()
                    set_current_version(installed)
                if line.strip().startswith(b"LATEST:"):
                    latest = line.split(b":")[1].strip().decode()
                    set_latest_version(latest)

            # Output wasn't parse properly, or package isn't installed
            if not installed or not latest:
                set_error_msg("Error. Check logs.")
                _logger.error(
                    "Failed to parse 'pip index versions' for %s: %s",
                    pkg_name,
                    stdout,
                )

            proc.kill()

        threading.Thread(target=thread_func, daemon=True).start()

    status = ""
    if error_msg:
        status = "text-danger"
    if latest_version and current_version:
        status = "text-success" if latest_version == current_version else "text-warning"

    return html.tr(
        html.td(pkg_name),
        html.td(
            html.div(
                {"class_name": status}, error_msg or current_version or "Checking..."
            )
        ),
        html.td(html.div("N/A" if error_msg else latest_version or "Checking...")),
        html.td(
            {"style": {"text-align": "center"}}, html.i({"class_name": "fas fa-cog"})
        ),
    )
