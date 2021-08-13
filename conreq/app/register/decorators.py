from functools import wraps

from channels.consumer import AsyncConsumer
from huey.contrib.djhuey import db_periodic_task, db_task

from conreq.app import AuthLevel, Icon, Navtab, Viewport

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable


def websocket(path: str, regex: bool = False):
    def decorator(_class: AsyncConsumer):
        @wraps(_class)
        def _wrapped_class(*args, **kwargs):
            return _wrapped_class(*args, **kwargs)


def url(path: str, regex: bool = False):
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
    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def api(path: str, version: int, auth: bool = True, regex: bool = False):
    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def server_settings(page_name: str):
    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def user_settings(admin_only: bool = False):
    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


# component = idom_component

task = db_task

periodic_task = db_periodic_task
