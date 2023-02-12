from conreq import config
from conreq.config.utils import tab_constructor
from conreq.config.wrappers.components import (
    app_store,
    server_settings,
    server_settings_email,
    server_settings_general,
    server_settings_licenses,
    server_settings_styling,
    server_settings_system_info,
    server_settings_webserver,
    sign_out,
    sign_out_event,
    user_management,
    user_management_create_invite,
    user_management_manage_invites,
    user_management_manage_users,
    user_settings,
    user_settings_change_password,
    user_settings_delete_account,
    user_settings_general,
)
from conreq.types import SubTab

# Register the component wrappers to be referenced by apps to change tabs
# Register the tabs and sidebar navtabs
# pylint: disable=protected-access
config.tabs.user_settings.main = tab_constructor("Settings", user_settings)
config._homepage.user_sidebar_tabs.append(config.tabs.user_settings.main)


config.tabs.sign_out.main = tab_constructor(
    "Sign Out", sign_out, on_click=sign_out_event
)
config._homepage.user_sidebar_tabs.append(config.tabs.sign_out.main)


config.tabs.user_management.main = tab_constructor("User Management", user_management)
config._homepage.admin_sidebar_tabs.append(config.tabs.user_management.main)


config.tabs.app_store.main = tab_constructor(
    "App Store", app_store, html_class="app-store", padding=False
)
config._homepage.admin_sidebar_tabs.append(config.tabs.app_store.main)


config.tabs.server_settings.main = tab_constructor("Server Settings", server_settings)
config._homepage.admin_sidebar_tabs.append(config.tabs.server_settings.main)


config.tabs.user_settings.general = SubTab(
    name="General", component=user_settings_general
)
config._internal_tabs.user_settings_top.append(config.tabs.user_settings.general)


config.tabs.user_settings.change_password = SubTab(
    name="Change Password", component=user_settings_change_password
)
config._internal_tabs.user_settings_top.append(
    config.tabs.user_settings.change_password
)


config.tabs.user_settings.delete_account = SubTab(
    name="Delete My Account", component=user_settings_delete_account
)
config._internal_tabs.user_settings_bottom.append(
    config.tabs.user_settings.delete_account
)


config.tabs.user_management.manage_users = SubTab(
    name="Manage Users", component=user_management_manage_users
)
config._internal_tabs.user_management.append(config.tabs.user_management.manage_users)


config.tabs.user_management.manage_invites = SubTab(
    name="Manage Invites", component=user_management_manage_invites
)
config._internal_tabs.user_management.append(config.tabs.user_management.manage_invites)


config.tabs.user_management.create_invite = SubTab(
    name="Create Invite", component=user_management_create_invite
)
config._internal_tabs.user_management.append(config.tabs.user_management.create_invite)


config.tabs.server_settings.general = SubTab(
    name="General", component=server_settings_general
)
config._internal_tabs.server_settings.append(config.tabs.server_settings.general)


config.tabs.server_settings.styling = SubTab(
    name="Styling", component=server_settings_styling
)
config._internal_tabs.server_settings.append(config.tabs.server_settings.styling)


config.tabs.server_settings.webserver = SubTab(
    name="Webserver", component=server_settings_webserver
)
config._internal_tabs.server_settings.append(config.tabs.server_settings.webserver)


config.tabs.server_settings.email = SubTab(
    name="Email", component=server_settings_email
)
config._internal_tabs.server_settings.append(config.tabs.server_settings.email)


config.tabs.server_settings.system_info = SubTab(
    name="System Info", component=server_settings_system_info
)
config._internal_tabs.server_settings.append(config.tabs.server_settings.system_info)


config.tabs.server_settings.licenses = SubTab(
    name="Licenses", component=server_settings_licenses
)
config._internal_tabs.server_settings.append(config.tabs.server_settings.licenses)
