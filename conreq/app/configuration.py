"""Conreq's configuration values."""

from dataclasses import dataclass, field
from typing import Callable


def view_stub(request):
    """Empty view function, to be populated later via app.register"""


@dataclass
class _Config:
    # Startup
    pre_run: list[Callable] = field(default_factory=list)
    setting_scripts: list[str] = field(default_factory=list)
    installed_apps: list[str] = field(default_factory=list)
    middlewares: list[dict] = field(default_factory=list)

    # Views
    # TODO: Make view wrappers for each of these.
    landing_view: Callable = view_stub
    home_view: Callable = view_stub
    sign_up_view: Callable = view_stub
    sign_in_view: Callable = view_stub
    password_reset_view: Callable = view_stub

    # Templates
    landing_template: str = ""
    home_template: str = "homepage/home.html"
    sign_up_template: str = "registration/sign_up.html"
    sign_in_template: str = "registration/sign_in.html"
    password_reset_template: str = ""
    loading_animation_template: str = "loading/spinner.html"

    # IDOM Components
    manage_users_component: Callable = None
    server_settings_component: Callable = None
    user_setting_sections: list[Callable] = field(default_factory=list)
    server_setting_tabs: list[dict] = field(default_factory=list)
    nav_tabs: dict[str, dict[str, Callable]] = field(default_factory=dict)

    # ASGI
    websockets: list[Callable] = field(default_factory=list)

    # WSGI (API and URLs)
    url_patterns: list = field(default_factory=list)

    # HTML Head
    local_stylesheets: list[dict] = field(default_factory=list)
    remote_stylesheets: list[dict] = field(default_factory=list)
    scss_stylesheets: list[dict] = field(default_factory=list)
    local_scripts: list[dict] = field(default_factory=list)
    remote_scripts: list[dict] = field(default_factory=list)
    head_content: list = field(default_factory=list)
