from typing import Callable

from conreq import config
from conreq.types import SubTab


def user_settings(name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the user settings page."""

    def decorator(func):
        config.tabs.user_settings.append(SubTab(name=name, component=func))
        return func

    return decorator


def manage_users(name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the manage users page."""

    def decorator(func):
        config.tabs.user_management.append(SubTab(name=name, component=func))
        return func

    return decorator


def app_store(name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the app store page."""

    def decorator(func):
        config.tabs.app_store.append(SubTab(name=name, component=func))
        return func

    return decorator


def server_settings(name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the user server settings page."""

    def decorator(func):
        config.tabs.server_settings.append(SubTab(name=name, component=func))
        return func

    return decorator
