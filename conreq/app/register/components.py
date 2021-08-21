from functools import wraps

from conreq.app import AuthLevel, Icon, Navtab, Viewport

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable


def navtab(
    selector: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
    nav_tab: Navtab = None,
    group_icon: Icon = None,
    icon_left: Icon = None,
    icon_right: Icon = None,
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


def user_settings(admin_only: bool = False) -> object:
    """Decorates an IDOM component. Component is injected into the user settings modal."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)
