import asyncio
import subprocess
import threading
import time
from typing import Sequence, Union, cast

from reactpy import component, hooks, html
from reactpy_django.components import django_css

from conreq._core.app_store.models import AppPackage, DevelopmentStage, Screenshot
from conreq._core.home.components.modal import (
    modal_body,
    modal_content,
    modal_dialog,
    modal_footer,
    modal_head,
)
from conreq.types import ModalStateContext


@component
def app_details_modal(app: AppPackage):
    modal_state = hooks.use_context(ModalStateContext)

    async def install_click(_):
        modal_state.modal_intent = app_install_modal
        modal_state.modal_args = [app]
        modal_state.set_state(modal_state)

    package_details = {
        "Development Stage": dict(DevelopmentStage.choices).get(
            app.development_stage, ""
        ),
        "Subcategories": ", ".join(
            [str(subcat.name) for subcat in app.subcategories.all()]
        ),
        "Author": text_to_link(app.author_url, app.author)
        if app.author_url
        else app.author,
        "Contact Email": text_to_link(f"mailto:{app.contact_email}", app.contact_email)
        if app.contact_email
        else "",
        "Contact Link": text_to_link(app.contact_link),
        "PyPI URL": text_to_link(app.pypi_url),
        "Repository URL": text_to_link(app.repository_url),
        "Homepage URL": text_to_link(app.homepage_url),
        "Support URL": text_to_link(app.support_url),
        "Donation URL": text_to_link(app.donation_url),
        "License Type": app.license_type,
    }
    compatibility = {
        "Supported Platforms": app.sys_platforms,
        "Touch Compatible": app.touch_compatible,
        "Mobile Compatible": app.mobile_compatible,
        "Minimum Package Version": app.min_version,
        "Conreq Minimum Version": app.conreq_min_version,
        "Conreq Maximum Version": app.conreq_max_version,
        "Asynchronous Support": app.asynchronous,
        "Required Apps": app.required_apps.all(),
        "Incompatible Apps": app.incompatible_apps.all(),
        "Related Apps": app.related_apps.all(),
    }

    return modal_dialog(
        modal_content(
            modal_head(title=app.name),
            modal_body(
                html.div(
                    {"class_name": "banner"}, "This app has not been developed yet!"
                )
                if not app.development_stage
                or app.development_stage == DevelopmentStage.PLANNING
                else "",
                html.div({"class_name": "banner"}, app.banner_message)
                if app.banner_message
                else "",
                screenshot_carousel(app.screenshot_set.all())
                if app.screenshot_set.all()
                else "",
                html.p(
                    {"class_name": "description"},
                    html.h5("Description"),
                    app.long_description,
                )
                if app.long_description
                else "",
                info_table("Package Details", package_details),
                info_table("Compatibility", compatibility),
            ),
            modal_footer(
                html.button(
                    {"class_name": "btn btn-primary", "on_click": install_click},
                    "Install",
                )
                if app.installable
                else ""
            ),
        ),
        django_css("conreq/app_details_modal.css"),
    )


@component
def info_table(title: str, info: dict):
    return html.div(
        {"class_name": "info-table-container"},
        html.h5({"class_name": "info-table-title"}, title),
        html.table(
            {"class_name": "info-table"},
            html.tbody(
                [
                    html.tr(
                        {"key": section_name},
                        html.th(section_name),
                        html.td(value),
                    )
                    for section_name, value in info.items()
                    if value
                ]
            ),
        ),
    )


@component
def screenshot_carousel(screenshots: Sequence[Screenshot]):
    """Converts a list of screenshots into a Bootstrap 5 carousel with indicators  and controls."""

    return html.div(
        {
            "id": "screenshot-carousel",
            "class_name": "carousel slide carousel-fade",
            "data-bs-ride": "carousel",
        },
        html.div(
            {"class_name": "carousel-indicators"},
            [
                html.button(
                    {
                        "type": "button",
                        "data-bs-target": "#screenshot-carousel",
                        "data-bs-slide-to": str(i),
                        "class_name": "active" if i == 0 else "",
                        "aria-current": "true" if i == 0 else "false",
                        "aria-label": f"Slide {i + 1}",
                        "key": i,
                    },
                )
                for i in range(len(screenshots))
            ],
        ),
        html.div(
            {"class_name": "carousel-inner"},
            [
                html.div(
                    {
                        "class_name": "carousel-item active"
                        if i == 0
                        else "carousel-item",
                        "key": str(screenshot.uuid),
                        "data-bs-interval": 10000,
                    },
                    html.img(
                        {
                            "src": screenshot.image.url,
                            "class_name": "d-block",
                            "alt": screenshot.description,
                        }
                    ),
                    html.div(
                        {"class_name": "carousel-caption d-none d-md-block"},
                        html.h5(screenshot.title),
                        html.p(screenshot.description),
                    ),
                )
                for i, screenshot in enumerate(screenshots)
            ],
        ),
    )


def text_to_link(link_str: str, text_str: str = ""):
    """Converts a string into a link if possible, otherwise return None."""

    return html.a({"href": link_str}, text_str or link_str) if link_str else None


@component
def app_install_modal(app: AppPackage):
    cmd = ["pip", "install", app.pkg_name, "--disable-pip-version-check"]
    confirmed, set_confirmed = hooks.use_state(False)
    cancelled, set_cancelled = hooks.use_state(False)
    proc, set_proc = hooks.use_state(cast(Union[subprocess.Popen, None], None))
    stdout, set_stdout = hooks.use_state(html.p(" ".join(cmd)))
    retcode, set_retcode = hooks.use_state(cast(Union[int, None], None))
    modal_state = hooks.use_context(ModalStateContext)

    async def close_modal(_):
        print("close")
        modal_state.show = False
        modal_state.set_state(modal_state)

    @hooks.use_effect
    def install_app():
        if confirmed and not proc:
            set_proc(
                subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
            )

        if proc and cancelled:
            proc.kill()

    @hooks.use_effect(dependencies=[proc, stdout])
    async def update_stdout():
        if not proc:
            return

        def thread_func():
            if not proc:
                return
            if proc.poll() is None:
                if not proc.stdout:
                    set_stdout(
                        html.p("An error has occurred. Unable to read output shell.")
                    )
                    return
                set_stdout(
                    html._(stdout, html.p(proc.stdout.readline().decode("utf-8")))
                )

        threading.Thread(target=thread_func, daemon=True).start()

    @hooks.use_effect(dependencies=[proc])
    async def update_retcode():
        if not proc:
            return

        def thread_func():
            if not proc:
                return
            proc.wait()
            set_retcode(proc.returncode)

        threading.Thread(target=thread_func, daemon=True).start()

    return modal_dialog(
        modal_content(
            modal_head(title=f"Installing: {app.name}"),
            modal_body(
                html.div(
                    {"class_name": "terminal", "key": "terminal"},
                    stdout,
                    [
                        html.p(
                            {"key": "success"},
                            "Success. A restart is required to use this app.",
                        )
                        if retcode == 0
                        else html.p(
                            {"key": "failure"},
                            "An error occurred during installation.",
                        )
                    ]
                    if retcode is not None
                    else "",
                )
                if confirmed
                else html.div(
                    {"class_name": "confirm", "key": "confirm"},
                    "Are you sure you want to install ",
                    html.b(app.name),
                    "?",
                )
            ),
            modal_footer(
                [
                    html.button(
                        {
                            "class_name": "btn btn-secondary",
                            "disabled": True,
                            "key": "restart",
                        },
                        "Restart Required",
                    )
                    if retcode == 0
                    else ""
                ]
                if retcode is not None
                else html.button(
                    {
                        "class_name": "btn btn-danger",
                        "on_click": lambda _: set_cancelled(True),
                        "key": "cancel",
                    },
                    "Cancel",
                )
                if confirmed
                else html._(
                    html.button(
                        {
                            "class_name": "btn btn-primary",
                            "on_click": lambda _: set_confirmed(True),
                            "key": "yes",
                        },
                        "Yes",
                    ),
                    html.button(
                        {
                            "class_name": "btn btn-danger",
                            "data-bs-dismiss": "modal",
                            "aria-label": "Close",
                            "on_click": close_modal,
                            "key": "no",
                        },
                        "No",
                    ),
                ),
            ),
        ),
        django_css("conreq/app_install_modal.css"),
    )
