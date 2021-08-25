"""Conreq's configuration values."""

from dataclasses import dataclass
from typing import Callable


@dataclass
class Config:
    # Startup
    pre_run: list = []
    pre_startup: list = []
    setting_scripts: list = []
    installed_apps: list = []
    middleware: list = []
    landing_template: str = ""
    landing_view: Callable = None
    home_template: str = ""
    home_view: Callable = None
    sign_up_template: str = ""
    sign_up_view: Callable = None
    sign_in_template: str = ""
    sign_in_view: Callable = None
    password_reset_template: str = ""
    password_reset_view: Callable = None
    manage_users_component: Callable = None
    server_settings_component: Callable = None

    # ASGI
    websockets: list = []

    # WSGI
    api_endpoints: list = []
    url_patterns: list = []

    # Components
    navtabs: list = []
    server_setting_tabs: list = []
    user_setting_components: list = []

    # HTML Head
    css: list = []
    scss: list = []
    javascript: list = []
    fonts: list = []
    head_content: list = []
