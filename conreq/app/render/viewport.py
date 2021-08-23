"""Helpers to render IDOM elements on the page"""
from functools import wraps

from conreq.app import AuthLevel, Icon, Navtab, Viewport

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable,unnecessary-pass


def viewport(
    selector: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
    nav_tab: Navtab = None,
    group_icon: Icon = None,
    icon_left: Icon = None,
    icon_right: Icon = None,
) -> object:
    """Decorates an IDOM component. Forcibly changes the viewport content."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)
