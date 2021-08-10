from functools import wraps

from huey.contrib.djhuey import db_periodic_task, db_task

AUTH_ANONYMOUS = 0
AUTH_USER = 1
AUTH_ADMIN = 2

# TODO: Create decorators
# pylint: disable=unused-argument,unused-variable


def url(path: str, regex: bool = False):
    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            pass


def nav_tab(
    page_name: str,
    group_name: str,
    auth_level: int = 1,
    group_icon_cls: str = None,
    group_icon_txt: str = None,
    icon_left_cls: str = None,
    icon_left_txt: str = None,
    icon_right_cls: str = None,
    icon_right_txt: str = None,
):
    def decorator(func):
        @wraps(func)
        def _wrapped_func():
            pass


def api(path: str, version: int, regex: bool = False):
    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            pass


def server_settings(page_name: str):
    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            pass


def user_settings(admin_only: bool = False):
    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            pass


def middleware(position_to: str = None, position_after: bool = True):
    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            pass


def component():
    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            pass


task = db_task

periodic_task = db_periodic_task
