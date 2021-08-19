"""Helpers to render IDOM elements on the page"""
from functools import wraps

from conreq.app import AuthLevel, Icon, Navtab, Viewport

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable,unnecessary-pass


def toast_message(
    title: str,
    message: str,
    icon: str,
    params: dict = None,
):
    """Renders a toast message with a specific message."""

    pass


def modal():
    """Decorates a Modal class type (not yet created)."""

    def decorator(class_: object):
        @wraps(class_)
        def _wrapped_class(*args, **kwargs):
            return _wrapped_class(*args, **kwargs)


def viewport(
    selector: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
    nav_tab: Navtab = None,
    group_icon: Icon = None,
    icon_left: Icon = None,
    icon_right: Icon = None,
):
    """Decorates an IDOM component. Forcibly changes the viewport content."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)
