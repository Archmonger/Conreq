from idom import component, html

from conreq._core.app_store.models import AppPackage
from conreq._core.home.components.modal import (
    modal_body,
    modal_content,
    modal_dialog,
    modal_footer,
    modal_head,
)


@component
def app_modal(app: AppPackage):
    app_details = (
        "Package Details",
        f"Development Stage: {app.development_stage}",
        f"Subcategories: {app.subcategories.all()}",
        f"Related Apps: {app.related_apps.all()}",
        "Ownership Details",
        f"Author: {app.author}",
        f"Author URL: {app.author_url}",
        f"Contact Email: {app.contact_email}",
        f"Contact Link: {app.contact_link}",
        f"PyPI URL: {app.pypi_url}",
        f"Repository URL: {app.repository_url}",
        f"Homepage URL: {app.homepage_url}",
        f"Support URL: {app.support_url}",
        f"Donation URL: {app.donation_url}",
        f"License Type: {app.license_type}",
        "Compatibility",
        f"Supported Platforms: {app.sys_platforms}",
        f"Touch Compatible: {app.touch_compatible}",
        f"Mobile Compatible: {app.mobile_compatible}",
        f"Minimum Package Version: {app.min_version}",
        f"Conreq Minimum Version: {app.conreq_min_version}",
        f"Conreq Maximum Version: {app.conreq_max_version}",
        f"Asynchronous Support: {app.asynchronous}",
        f"Required Apps: {app.required_apps.all()}",
        f"Incompatible Apps: {app.incompatible_apps.all()}",
    )

    return modal_dialog(
        modal_content(
            modal_head(title=app.name),
            modal_body(
                html.div(app.banner_message),
                html.div(f"Screenshots: {app.screenshot_set.all()}"),
                html.div(app.long_description),
                html.div(html.button("show more")),
                [html.p(app_str, key=app_str) for app_str in app_details],
            ),
            modal_footer(),
        )
    )
