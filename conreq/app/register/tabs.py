from conreq import config
from conreq.types import SubTab


def user_settings(name: str):
    """Decorates an IDOM component. Tabs are added to the user settings page."""

    def decorator(func):
        config.tabs.user_settings.installed.append(SubTab(name=name, component=func))
        return func

    return decorator


def manage_users(name: str):
    """Decorates an IDOM component. Tabs are added to the manage users page."""

    def decorator(func):
        config.tabs.user_management.installed.append(SubTab(name=name, component=func))
        return func

    return decorator


def server_settings(name: str):
    """Decorates an IDOM component. Tabs are added to the user server settings page."""

    def decorator(func):
        config.tabs.server_settings.installed.append(SubTab(name=name, component=func))
        return func

    return decorator
