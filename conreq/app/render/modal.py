"""Helpers to render IDOM elements on the page"""
from functools import wraps

from conreq.app import AuthLevel, Icon, Navtab, Viewport


# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable,unnecessary-pass


def modal() -> object:
    """Decorates a Modal class (not yet created)."""

    def decorator(class_: object):
        @wraps(class_)
        def _wrapped_class(*args, **kwargs):
            return _wrapped_class(*args, **kwargs)
