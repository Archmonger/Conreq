from typing import Callable

from conreq import config
from conreq.app.types import Tab


def user_settings(name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the user settings page."""

    def decorator(func):
        config.tabs.user_settings.append(Tab(name=name, component=func))
        return func

    return decorator


def manage_users(name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the manage users page."""

    def decorator(func):
        config.tabs.manage_users.append(Tab(name=name, component=func))
        return func

    return decorator


def app_store(name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the app store page."""

    def decorator(func):
        config.tabs.app_store.append(Tab(name=name, component=func))
        return func

    return decorator


def server_settings(name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the user server settings page."""

    def decorator(func):
        config.tabs.server_settings.append(Tab(name=name, component=func))
        return func

    return decorator