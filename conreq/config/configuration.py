"""Conreq's configuration values."""

from dataclasses import dataclass, field
from typing import Callable

from idom.core.proto import VdomDict
from idom.html import div, span
from sortedcontainers import SortedList

from conreq.config import view_wrappers
from conreq.app.types import NavGroup, NavTab, Tab
from conreq.utils.containers import FillList


@dataclass
class StartupConfig:
    setting_scripts: set[str] = field(default_factory=set)
    # TODO: Implement pre_run scripts
    pre_run: set[Callable] = field(default_factory=set)


@dataclass
class ViewConfig:
    # TODO: Don't use the app.register API for pre-configuring the base views here
    landing: Callable = view_wrappers.landing
    home: Callable = view_wrappers.home
    sign_up: Callable = view_wrappers.sign_up
    sign_in: Callable = view_wrappers.sign_in
    password_reset: Callable = view_wrappers.password_reset
    password_reset_sent: Callable = view_wrappers.password_reset_sent
    password_reset_confirm: Callable = view_wrappers.password_reset_confirm


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
    # TODO: Implement these components (needs wrappers)
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
    user_settings: SortedList[Tab] = field(default_factory=SortedList)
    manage_users: SortedList[Tab] = field(default_factory=SortedList)
    app_store: SortedList[Tab] = field(default_factory=SortedList)
    server_settings: SortedList[Tab] = field(default_factory=SortedList)


@dataclass
class _InternalTabConfig:
    user_settings_top: list[Tab] = field(default_factory=list)
    user_settings_bottom: list[Tab] = field(default_factory=list)
    manage_users: list[Tab] = field(default_factory=list)
    server_settings: list[Tab] = field(default_factory=list)


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
    nav_tabs: SortedList[NavGroup] = field(default_factory=SortedList)
    default_nav_tab: NavTab = None
    # TODO: Implement CSS and JS registration
    local_stylesheets: list[dict] = field(default_factory=list)
    remote_stylesheets: list[dict] = field(default_factory=list)
    scss_stylesheets: list[dict] = field(default_factory=list)
    local_scripts: list[dict] = field(default_factory=list)
    remote_scripts: list[dict] = field(default_factory=list)
    head_content: list[str] = field(default_factory=list)


@dataclass
class _InternalHomepageConfig:
    user_nav_tabs: list[NavTab] = field(default_factory=list)
    admin_nav_tabs: FillList[NavTab] = field(default_factory=FillList)
    debug_nav_tabs: list[NavTab] = field(default_factory=list)
