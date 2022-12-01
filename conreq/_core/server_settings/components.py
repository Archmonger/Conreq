import platform
import sys
from os.path import relpath
from uuid import uuid4

import channels
import django
from django.conf import settings
from django_idom.components import view_to_component
from django_idom.decorators import auth_required
from idom import component, html

from conreq import config
from conreq._core.components import tabbed_viewport
from conreq._core.server_settings import views

# TODO: Create generic notification agent API.

general_settings_vtc = view_to_component(views.GeneralSettingsView, compatibility=True)
styling_settings_vtc = view_to_component(views.StylingSettingsView, compatibility=True)
webserver_settings_vtc = view_to_component(
    views.WebserverSettingsView, compatibility=True
)
email_settings_vtc = view_to_component(views.EmailSettingsView, compatibility=True)


@component
@auth_required(auth_attribute="is_staff")
def general_settings():
    return general_settings_vtc()


@component
@auth_required(auth_attribute="is_staff")
def styling_settings():
    return styling_settings_vtc()


@component
@auth_required(auth_attribute="is_staff")
def webserver_settings():
    return webserver_settings_vtc()


@component
@auth_required(auth_attribute="is_staff")
def email_settings():
    return email_settings_vtc()


def system_info():

    settings_values = [
        ("Conreq Version", settings.CONREQ_VERSION),
        ("Configuration File", relpath(settings.DOTENV_FILE)),
        ("Cache Directory", relpath(settings.CACHES["default"]["LOCATION"])),
        ("Conreq Log File", relpath(settings.CONREQ_LOG_FILE)),
        ("Webserver Log File", relpath(settings.ACCESS_LOG_FILE)),
        ("Database File", relpath(settings.DATABASES["default"]["NAME"])),
        ("Log Level", settings.LOG_LEVEL),
        ("Platform", platform.platform()),
        ("CPU Architecture", platform.machine()),
        ("System Timezone", settings.TIME_ZONE),
        ("Django Version", django.get_version()),
        ("Channels Version", channels.__version__),
        ("Python Version", platform.python_version()),
        ("Python Arguments", " ".join(sys.argv)),
    ]

    return html.table(
        {"style": {"marginTop": "20px"}},
        [
            html.tr(html.td(f"{name}"), html.td(f"{value}"), key=uuid4().hex)
            for name, value in settings_values
        ],
    )


def licenses():
    return html.div(
        {"style": {"marginTop": "20px"}},
        "This page is under construction, and will be developed in a later release.",
    )


# pylint: disable=protected-access
@component
def server_settings():
    return html._(
        tabbed_viewport(
            tabs=config.tabs.server_settings.installed,
            top_tabs=config._internal_tabs.server_settings,
        )
    )
