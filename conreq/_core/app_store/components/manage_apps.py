import subprocess
import threading
from logging import getLogger
from typing import cast

from reactpy import component, hooks, html
from reactpy_django.components import django_css

from conreq.utils.environment import get_env, set_env
from conreq.utils.packages import find_packages

_logger = getLogger(__name__)


@component
def manage_apps():
    """Bootstrap table for managing apps."""

    installed_packages = find_packages(show_disabled=True)

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
                    html.th("Disabled"),
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
    available_versions, set_available_versions = hooks.use_state(cast(list[str], []))
    disabled_packages, set_disabled_packages = hooks.use_state(
        sorted(set(get_env("DISABLED_PACKAGES", [], return_type=list)))
    )

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
                set_error_msg("ERROR")
                _logger.error(
                    "Broken stderr or stdout while getting pip index versions for %s",
                    pkg_name,
                )
                return

            # Check if pip index versions failed
            stderr = proc.stderr.readlines()
            for line in stderr:
                if line.strip().startswith(b"ERROR:"):
                    set_error_msg("ERROR")
                    _logger.error(
                        "'pip index versions' failed for %s: %s",
                        pkg_name,
                        line.strip().decode()[7:],
                    )
                    return

            # Parse output
            stdout = proc.stdout.readlines()
            versions: list[str] = []
            installed: str = ""
            latest: str = ""
            for line in stdout:
                if line.strip().startswith(b"Available versions:"):
                    versions = line.split(b":")[1].strip().decode().split(", ")
                    latest = versions[0]
                if line.strip().startswith(b"INSTALLED:"):
                    installed = line.split(b":")[1].strip().decode()
                if line.strip().startswith(b"LATEST:"):
                    latest = line.split(b":")[1].strip().decode()
            if versions:
                set_available_versions(versions)
            if installed:
                set_current_version(installed)
            if latest:
                set_latest_version(latest)

            # Output wasn't parsed properly, or package isn't installed
            if not installed:
                set_error_msg("ERROR")
                _logger.error(
                    "Failed to obtain currently installed version from 'pip index versions' for %s: %s",
                    pkg_name,
                    stdout,
                )
            if not versions:
                _logger.error(
                    "Failed to obtain versions list from 'pip index versions' for %s: %s",
                    pkg_name,
                    stdout,
                )
            if not latest:
                _logger.error(
                    "Failed to obtain latest version from 'pip index versions' for %s: %s",
                    pkg_name,
                    stdout,
                )

            proc.kill()

        threading.Thread(target=thread_func, daemon=True).start()

    async def disable_click(_):
        if pkg_name in disabled_packages:
            disabled_packages.remove(pkg_name)
        else:
            disabled_packages.append(pkg_name)
        set_env("DISABLED_PACKAGES", disabled_packages)
        set_disabled_packages(sorted(disabled_packages))

    status = ""
    if error_msg:
        status = "text-danger"
    if latest_version and current_version:
        status = "" if latest_version == current_version else "text-warning"

    return html.tr(
        html.td(pkg_name),
        html.td(
            html.div(
                {"class_name": status}, error_msg or current_version or "Checking..."
            )
        ),
        html.td(latest_version or ("N/A" if error_msg else "Checking...")),
        html.td("Yes" if pkg_name in disabled_packages else "No"),
        html.td(
            {"style": {"text-align": "center"}},
            html.div(
                {"class_name": "dropdown"},
                html.button(
                    {
                        "class_name": "btn btn-sm btn-dark dropdown-toggle",
                        "type": "button",
                        "data-bs-toggle": "dropdown",
                        "aria-expanded": "false",
                    },
                    html.i({"class_name": "fas fa-cog"}),
                ),
                html.ul(
                    {"class_name": "dropdown-menu"},
                    dropdown_item("Update", lambda _: None)
                    if latest_version != current_version
                    else "",
                    dropdown_item("Uninstall", lambda _: None),
                    dropdown_item(
                        "Enable" if pkg_name in disabled_packages else "Disable",
                        disable_click,
                    ),
                    dropdown_item("Change Version", lambda _: None)
                    if available_versions
                    else "",
                ),
            ),
        ),
    )


def dropdown_item(option: str, on_click):
    return html.li(
        {"key": option},
        html.a(
            {
                "class_name": "dropdown-item",
                "href": f"#{option}",
                "on_click": on_click,
            },
            f"{option}",
        ),
    )
