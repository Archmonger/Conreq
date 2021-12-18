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
        password_reset_confirm,
        password_reset_sent,
        sign_in,
        sign_up,
    )

    # Startup
    pre_run: set[Callable] = field(default_factory=set)
    setting_scripts: set[str] = field(default_factory=set)

    # Views
    # TODO: Don't use the app.register API for pre-configuring the base views here
    landing_view: Callable = landing
    home_view: Callable = home
    sign_up_view: Callable = sign_up
    sign_in_view: Callable = sign_in
    password_reset_view: Callable = password_reset
    password_reset_sent_view: Callable = password_reset_sent
    password_reset_confirm_view: Callable = password_reset_confirm

    # Templates
    landing_template: str = ""
    home_template: str = "conreq/homepage/home.html"
    sign_up_template: str = "conreq/registration/sign_up.html"
    sign_in_template: str = "conreq/registration/sign_in.html"
    password_reset_template: str = "conreq/registration/password_reset.html"
    password_reset_sent_template: str = "conreq/registration/password_reset_sent.html"
    password_reset_confirm_template: str = (
        "conreq/registration/password_reset_confirm.html"
    )

    # IDOM Components
    # TODO: Implement these components
    manage_users_component: Callable = None
    server_settings_component: Callable = None
    user_settings_component: Callable = None
    app_store_component: Callable = None
    user_setting_tabs: dict[str, dict[str, Callable]] = field(default_factory=dict)
    server_setting_tabs: dict[str, dict[str, Callable]] = field(default_factory=dict)
    nav_tabs: dict[str, dict[str, Callable]] = field(default_factory=dict)

    # IDOM VDOMs
    loading_animation_vdom: VdomDict = field(
        default_factory=lambda: div(
            {"className": "spinner-border loading-animation", "role": "status"},
            span({"className": "sr-only"}, "Loading..."),
        ),
    )

    # WSGI
    # TODO: Implement WSGI middleware
    wsgi_middleware: set[dict] = field(default_factory=set)

    # ASGI
    websockets: list[Callable] = field(default_factory=list)
    # TODO: Implement ASGI middleware
    asgi_middleware: set[dict] = field(default_factory=set)

    # HTML Head
    # TODO: Implement CSS and JS registration
    home_local_stylesheets: list[dict] = field(default_factory=list)
    home_remote_stylesheets: list[dict] = field(default_factory=list)
    home_scss_stylesheets: list[dict] = field(default_factory=list)
    home_local_scripts: list[dict] = field(default_factory=list)
    home_remote_scripts: list[dict] = field(default_factory=list)
