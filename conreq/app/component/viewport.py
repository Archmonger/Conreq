from functools import wraps

from ..selectors import AuthLevel, Viewport
from .types import Icon, Navtab

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable


def navtab(
    selector: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
    nav_tab: Navtab = None,
    group_icon: Icon = None,
    icon: Icon = None,
    button: Icon = None,
) -> object:
    """Decorates an IDOM component. Tab is added to the sidebar and is rendered when clicked."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def server_settings(page_name: str) -> object:
    """Decorates an IDOM component. Creates a settings page."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)