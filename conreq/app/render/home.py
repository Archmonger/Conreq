"""Helpers to render IDOM elements on the page"""
from typing import Callable

from conreq import AuthLevel, Viewport

# TODO: Create viewport render functions
# pylint: disable=unused-argument,unused-variable,unnecessary-pass


def viewport(
    selector: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
) -> Callable:
    """Decorates an IDOM component. Forcibly changes the viewport content."""

    def decorator(func):
        return func

    return decorator


def background(css_string: str):
    """Changes the homescreen's background to a specific CSS string."""
