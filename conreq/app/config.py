"""Conreq's configuration values."""

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class _Config:
    # Startup
    pre_run: list = field(default_factory=list)
    pre_startup: list = field(default_factory=list)
    setting_scripts: list = field(default_factory=list)
    installed_apps: list = field(default_factory=list)
    middleware: list = field(default_factory=list)
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
    loading_animation_template: str = ""
    manage_users_component: Callable = None
    server_settings_component: Callable = None

    # ASGI
    websockets: list = field(default_factory=list)

    # WSGI
    api_endpoints: list = field(default_factory=list)
    url_patterns: list = field(default_factory=list)

    # Components
    navtabs: list = field(default_factory=list)
    server_setting_tabs: list = field(default_factory=list)
    user_setting_components: list = field(default_factory=list)

    # HTML Head
    css: list = field(default_factory=list)
    scss: list = field(default_factory=list)
    javascript: list = field(default_factory=list)
    fonts: list = field(default_factory=list)
    head_content: list = field(default_factory=list)


Config = _Config()
