"""Conreq's configuration values."""

from dataclasses import dataclass, field
from typing import Callable

from idom.core.proto import VdomDict
from idom.html import div, span


@dataclass
class _Config:
    # pylint: disable=too-many-instance-attributes, import-outside-toplevel
    from conreq.internal.view_wrappers.views import (
        home,
        landing,
        password_reset,
        sign_in,
        sign_up,
    )

    # Startup
    pre_run: set[Callable] = field(default_factory=set)
    setting_scripts: set[str] = field(default_factory=set)

    # Views
    landing_view: Callable = landing
    home_view: Callable = home
    sign_up_view: Callable = sign_up
    sign_in_view: Callable = sign_in
    password_reset_view: Callable = password_reset  # TODO: Implement this

    # Templates
    landing_template: str = ""
    home_template: str = "homepage/home.html"
    sign_up_template: str = "registration/sign_up.html"
    sign_in_template: str = "registration/sign_in.html"
    password_reset_template: str = ""  # TODO: Implement this

    # IDOM Components
    # TODO: Implement these
    manage_users_component: Callable = None
    server_settings_component: Callable = None
    user_settings_component: Callable = None
    user_setting_sections: list[Callable] = field(default_factory=list)
    server_setting_tabs: list[dict] = field(default_factory=list)
    nav_tabs: dict[str, dict[str, Callable]] = field(default_factory=dict)

    # IDOM VDOMs
    loading_animation_vdom: VdomDict = field(
        default_factory=lambda: div(
            {"className": "spinner-border loading-animation", "role": "status"},
            span({"className": "sr-only"}, "Loading..."),
        ),
    )

    # WSGI
    wsgi_middleware: set[dict] = field(default_factory=set)  # TODO: Implement this

    # ASGI
    websockets: list[Callable] = field(default_factory=list)
    asgi_middleware: set[dict] = field(default_factory=set)  # TODO: Implement this

    # HTML Head
    # TODO: Implement these
    home_local_stylesheets: list[dict] = field(default_factory=list)
    home_remote_stylesheets: list[dict] = field(default_factory=list)
    home_scss_stylesheets: list[dict] = field(default_factory=list)
    home_local_scripts: list[dict] = field(default_factory=list)
    home_remote_scripts: list[dict] = field(default_factory=list)
