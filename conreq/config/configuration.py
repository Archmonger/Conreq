"""Conreq's configuration values."""

from dataclasses import dataclass, field
from typing import Callable

from idom.core.proto import VdomDict
from idom.html import div, span

from conreq.internal.view_wrappers import views


@dataclass
class StartupConfig:
    setting_scripts: set[str] = field(default_factory=set)
    # TODO: Implement these startup configurations
    pre_run: set[Callable] = field(default_factory=set)
    installed_apps: set[str] = field(default_factory=set)


@dataclass
class ViewConfig:
    # TODO: Don't use the app.register API for pre-configuring the base views here
    landing: Callable = views.landing
    home: Callable = views.home
    sign_up: Callable = views.sign_up
    sign_in: Callable = views.sign_in
    password_reset: Callable = views.password_reset
    password_reset_sent: Callable = views.password_reset_sent
    password_reset_confirm: Callable = views.password_reset_confirm


@dataclass
class TemplateConfig:
    landing: str = ""
    home: str = "conreq/homepage/home.html"
    sign_up: str = "conreq/registration/sign_up.html"
    sign_in: str = "conreq/registration/sign_in.html"
    password_reset: str = "conreq/registration/password_reset.html"
    password_reset_sent: str = "conreq/registration/password_reset_sent.html"
    password_reset_confirm: str = "conreq/registration/password_reset_confirm.html"


@dataclass
class ComponentConfig:
    # TODO: Implement these components
    manage_users: Callable = None
    server_settings: Callable = None
    user_settings: Callable = None
    app_store: Callable = None
    loading_animation: VdomDict = field(
        default_factory=lambda: div(
            {"className": "spinner-border loading-animation", "role": "status"},
            span({"className": "sr-only"}, "Loading..."),
        ),
    )


@dataclass
class TabConfig:
    # TODO: Redo this as objects instead of dicts
    # TODO: Implement these tabs
    user_settings: dict[str, dict[str, Callable]] = field(default_factory=dict)
    manage_users: dict[str, dict[str, Callable]] = field(default_factory=dict)
    app_store: dict[str, dict[str, Callable]] = field(default_factory=dict)
    server_settings: dict[str, dict[str, Callable]] = field(default_factory=dict)


@dataclass
class WsgiConfig:
    # TODO: Implement WSGI middleware
    middleware: set[dict] = field(default_factory=set)


@dataclass
class AsgiConfig:
    websockets: list[Callable] = field(default_factory=list)
    # TODO: Implement ASGI middleware
    middleware: set[dict] = field(default_factory=set)


@dataclass
class HomepageConfig:
    nav_tab: dict[str, dict[str, Callable]] = field(default_factory=dict)
    # TODO: Implement CSS and JS registration
    local_stylesheets: list[dict] = field(default_factory=list)
    remote_stylesheets: list[dict] = field(default_factory=list)
    scss_stylesheets: list[dict] = field(default_factory=list)
    local_scripts: list[dict] = field(default_factory=list)
    remote_scripts: list[dict] = field(default_factory=list)
    head_content: list[str] = field(default_factory=list)
