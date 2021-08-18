from functools import wraps

from channels.consumer import AsyncConsumer
from conreq.app import AuthLevel, Icon, Navtab, Viewport

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable


def websocket(path: str, use_regex: bool = False):
    """Decorates a websocket consumer class."""

    def decorator(class_: AsyncConsumer):
        @wraps(class_)
        def _wrapped_class(*args, **kwargs):
            return _wrapped_class(*args, **kwargs)


def url(path: str, use_regex: bool = False):
    """Decorates a Django view function."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def navtab(
    selector: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
    nav_tab: Navtab = None,
    group_icon: Icon = None,
    icon_left: Icon = None,
    icon_right: Icon = None,
):
    """Decorates an IDOM component. Tab is added to the sidebar and is rendered when clicked."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def api(path: str, version: int, auth: bool = True, use_regex: bool = False):
    """Decorates a DRF view function."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def server_settings(page_name: str):
    """Decorates an IDOM component. Creates a settings page."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def user_settings(admin_only: bool = False):
    """Decorates an IDOM component. Component is injected into the user settings modal."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)
