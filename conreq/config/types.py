"""Conreq's configuration values."""

from dataclasses import dataclass, field
from typing import Callable

from idom.core.types import VdomDict
from idom.html import div, span
from sortedcontainers import SortedList

from conreq.types import NavGroup, NavTab, Tab
from conreq.utils.containers import FillList

# pylint: disable=too-many-instance-attributes


@dataclass
class StartupConfig:
    setting_scripts: set[str] = field(default_factory=set)
    # TODO: Implement pre_run scripts
    pre_run: set[Callable] = field(default_factory=set)


@dataclass
class ViewConfig:
    landing: Callable | None = None
    home: Callable | None = None
    sign_up: Callable | None = None
    sign_in: Callable | None = None
    password_reset: Callable | None = None
    password_reset_sent: Callable | None = None
    password_reset_confirm: Callable | None = None
    offline: Callable | None = None
    service_worker: Callable | None = None
    web_manifest: Callable | None = None


@dataclass
class TemplateConfig:
    # FIXME: Some of these don't respect the settings change
    landing: str = ""
    home: str = "conreq/home.html"
    sign_up: str = "conreq/sign_up.html"
    sign_in: str = "conreq/sign_in.html"
    password_reset: str = "conreq/password_reset.html"
    password_reset_sent: str = "conreq/password_reset_sent.html"
    password_reset_confirm: str = "conreq/password_reset_confirm.html"
    offline: str = "conreq/offline.html"


@dataclass
class _UserSettingsComponents:
    viewport: Callable | None = None
    general: Callable | None = None
    change_password: Callable | None = None
    delete_account: Callable | None = None


@dataclass
class _SignOutComponents:
    viewport: Callable | None = None
    event: Callable | None = None


@dataclass
class _UserManagementComponents:
    viewport: Callable | None = None
    manage_users: Callable | None = None
    manage_invites: Callable | None = None
    create_invite: Callable | None = None


@dataclass
class _AppStoreComponents:
    viewport: Callable | None = None


@dataclass
class _ServerSettingsComponents:
    viewport: Callable | None = None
    general: Callable | None = None
    styling: Callable | None = None
    webserver: Callable | None = None
    email: Callable | None = None
    system_info: Callable | None = None


@dataclass
class ComponentConfig:
    homepage: Callable | None = None
    user_settings: _UserSettingsComponents = field(
        default_factory=_UserSettingsComponents,
    )
    sign_out: _SignOutComponents = field(
        default_factory=_SignOutComponents,
    )
    user_management: _UserManagementComponents = field(
        default_factory=_UserManagementComponents,
    )
    app_store: _AppStoreComponents = field(
        default_factory=_AppStoreComponents,
    )
    server_settings: _ServerSettingsComponents = field(
        default_factory=_ServerSettingsComponents,
    )

    loading_animation: VdomDict = field(
        default_factory=lambda: div(
            {"className": "spinner-border loading-animation", "role": "status"},
            span({"className": "sr-only"}, "Loading..."),
        ),
    )
    loading_animation_large: VdomDict = field(
        default_factory=lambda: div(
            {"className": "spinner-border loading-animation lg", "role": "status"},
            span({"className": "sr-only"}, "Loading..."),
        ),
    )


@dataclass
class TabConfig:
    user_settings: SortedList[Tab] = field(default_factory=SortedList)
    user_management: SortedList[Tab] = field(default_factory=SortedList)
    app_store: SortedList[Tab] = field(default_factory=SortedList)
    server_settings: SortedList[Tab] = field(default_factory=SortedList)


@dataclass
class _InternalTabConfig:
    user_settings_top: list[Tab] = field(default_factory=list)
    user_settings_bottom: list[Tab] = field(default_factory=list)
    user_management: list[Tab] = field(default_factory=list)
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