from functools import wraps

from conreq.app.component.icon import Icon

from ..selectors import AuthLevel, Viewport

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable


def nav_group(
    group_name: str,
    group_icon: Icon = None,
):
    pass


def nav_tab(
    tab_name: str,
    group_name: str,
    selector: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
    icon: Icon = None,
) -> object:
    """Decorates an IDOM component. Tab is added to the sidebar and is rendered when clicked."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator


def server_setting(page_name: str) -> object:
    """Decorates an IDOM component. Creates a settings page."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator
