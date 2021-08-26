"""Conreq's configuration values."""

from dataclasses import dataclass, field
from typing import Callable

from conreq.core.base.views import home, landing
from conreq.core.sign_in.views import sign_in
from conreq.core.sign_up.views import sign_up


@dataclass
class _Config:
    # Startup
    pre_run: list[Callable] = field(default_factory=list)
    setting_scripts: list[str] = field(default_factory=list)
    installed_apps: list[str] = field(default_factory=list)
    middleware: list[str] = field(default_factory=list)

    # Views
    landing_view: Callable = landing
    home_view: Callable = home
    sign_up_view: Callable = sign_up
    sign_in_view: Callable = sign_in
    password_reset_view: Callable = None

    # Templates
    landing_template: str = ""
    home_template: str = "homepage/home.html"
    sign_up_template: str = "registration/sign_up.html"
    sign_in_template: str = "registration/sign_in.html"
    password_reset_template: str = ""
    loading_animation_template: str = "loading/spinner.html"

    # Components
    manage_users_component: Callable = None
    server_settings_component: Callable = None

    # ASGI
    websockets: list[Callable] = field(default_factory=list)

    # WSGI (API and URLs)
    url_patterns: list = field(default_factory=list)

    # Components
    nav_tabs: dict[str, dict] = field(default_factory=dict)
    server_setting_tabs: list[tuple[str, Callable]] = field(default_factory=list)
    user_setting_components: list[Callable] = field(default_factory=list)

    # HTML Head
    local_stylesheets: list[tuple[str, dict]] = field(default_factory=list)
    remote_stylesheets: list[tuple[str, dict]] = field(default_factory=list)
    scss_stylesheets: list[tuple[str, dict]] = field(default_factory=list)
    local_scripts: list[tuple[str, dict]] = field(default_factory=list)
    remote_scripts: list[tuple[str, dict]] = field(default_factory=list)
    head_content: list = field(default_factory=list)
