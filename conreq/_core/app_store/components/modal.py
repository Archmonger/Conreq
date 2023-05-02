from typing import Sequence

from reactpy import component, html
from reactpy_django.components import django_css

from conreq._core.app_store.models import AppPackage, DevelopmentStage, Screenshot
from conreq._core.home.components.modal import (
    modal_body,
    modal_content,
    modal_dialog,
    modal_footer,
    modal_head,
)


@component
def app_modal(app: AppPackage):
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
                html.button({"class_name": "btn btn-primary"}, "Install")
                if app.installable
                else ""
            ),
        ),
        django_css("conreq/app_modal.css"),
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
