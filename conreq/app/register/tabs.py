from typing import Callable

from conreq import config


def user_settings(tab_name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the user settings page."""

    def decorator(func):
        config.tabs.user_settings[tab_name] = {"component": func}
        return func

    return decorator


def manage_users(tab_name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the manage users page."""

    def decorator(func):
        config.tabs.manage_users[tab_name] = {"component": func}
        return func

    return decorator


def app_store(tab_name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the app store page."""

    def decorator(func):
        config.tabs.app_store[tab_name] = {"component": func}
        return func

    return decorator


def server_settings(tab_name: str) -> Callable:
    """Decorates an IDOM component. Tabs are added to the user server settings page."""

    def decorator(func):
        config.tabs.server_settings[tab_name] = {"component": func}
        return func

    return decorator
