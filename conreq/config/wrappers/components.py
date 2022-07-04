from inspect import iscoroutinefunction

import idom

from conreq import config


# pylint: disable=import-outside-toplevel
@idom.component
def homepage(*args, **kwargs):
    component = config.components.homepage
    if component is None:
        from conreq._core.home import components

        return components.homepage(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def user_settings(*args, **kwargs):
    component = config.components.user_settings.main
    if component is None:
        from conreq._core.user_settings import components

        return components.user_settings(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def user_settings_general(*args, **kwargs):
    component = config.components.user_settings.general
    if component is None:
        from conreq._core.user_settings import components

        return components.UserSettingsView(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def user_settings_change_password(*args, **kwargs):
    component = config.components.user_settings.change_password
    if component is None:
        from conreq._core.user_settings import components

        return components.ChangePasswordView(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def user_settings_delete_account(*args, **kwargs):
    component = config.components.user_settings.delete_account
    if component is None:
        from conreq._core.user_settings import components

        return components.DeleteMyAccountView(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def sign_out(*args, **kwargs):
    return config.components.sign_out.main


async def sign_out_event(*args, **kwargs):
    event = config.components.sign_out.event
    if event is None:
        from conreq._core.user_settings import components

        return await components.sign_out_event(*args, **kwargs)
    if iscoroutinefunction(event):
        return await event(*args, **kwargs)
    return event(*args, **kwargs)


@idom.component
def user_management(*args, **kwargs):
    component = config.components.user_management.main
    if component is None:
        from conreq._core.user_management import components

        return components.user_management(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def user_management_manage_users(*args, **kwargs):
    component = config.components.user_management.manage_users
    if component is None:
        from conreq._core.user_management import components

        return components.manage_users(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def user_management_manage_invites(*args, **kwargs):
    component = config.components.user_management.manage_invites
    if component is None:
        from conreq._core.user_management import components

        return components.manage_invites(*args, **kwargs)

    return component(*args, **kwargs)


@idom.component
def user_management_create_invite(*args, **kwargs):
    component = config.components.user_management.create_invite
    if component is None:
        from conreq._core.user_management import components

        return components.create_invite(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def app_store(*args, **kwargs):
    component = config.components.app_store.main
    if component is None:
        from conreq._core.app_store import components

        return components.app_store(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def server_settings(*args, **kwargs):
    component = config.components.server_settings.main
    if component is None:
        from conreq._core.server_settings import components

        return components.server_settings(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def server_settings_general(*args, **kwargs):
    component = config.components.server_settings.general
    if component is None:
        from conreq._core.server_settings import components

        return components.GeneralSettingsView(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def server_settings_styling(*args, **kwargs):
    component = config.components.server_settings.styling
    if component is None:
        from conreq._core.server_settings import components

        return components.StylingSettingsView(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def server_settings_webserver(*args, **kwargs):
    component = config.components.server_settings.webserver
    if component is None:
        from conreq._core.server_settings import components

        return components.WebserverSettingsView(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def server_settings_email(*args, **kwargs):
    component = config.components.server_settings.email
    if component is None:
        from conreq._core.server_settings import components

        return components.EmailSettingsView(*args, **kwargs)
    return component(*args, **kwargs)


@idom.component
def server_settings_system_info(*args, **kwargs):
    component = config.components.server_settings.system_info
    if component is None:
        from conreq._core.server_settings import components

        return components.system_info(*args, **kwargs)
    return component(*args, **kwargs)
