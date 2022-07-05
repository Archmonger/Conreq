"""Conreq's configuration values."""

from dataclasses import dataclass, field
from typing import Callable

from idom.html import div, span
from idom.types import ComponentType, VdomDict
from sortedcontainers import SortedList

from conreq.types import NavGroup, NavTab, Tab

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
    """Used to store user-defined components."""

    main: ComponentType | None = None
    general: ComponentType | None = None
    change_password: ComponentType | None = None
    delete_account: ComponentType | None = None


@dataclass
class _UserSettingsTabs:
    """Used to store NavTab/Tab objects for the default sidebar categories."""

    main: NavTab | None = None
    general: Tab | None = None
    change_password: Tab | None = None
    delete_account: Tab | None = None

    installed: SortedList[str] = field(default_factory=SortedList)


@dataclass
class _SignOutComponents:
    """Used to store user-defined components."""

    main: ComponentType | None = None
    event: Callable | None = None


@dataclass
class _SignOutTabs:
    """Used to store NavTab/Tab objects for the default sidebar categories."""

    main: NavTab | None = None


@dataclass
class _UserManagementComponents:
    """Used to store user-defined components."""

    main: ComponentType | None = None
    manage_users: ComponentType | None = None
    manage_invites: ComponentType | None = None
    create_invite: ComponentType | None = None


@dataclass
class _UserManagementTabs:
    """Used to store NavTab/Tab objects for the default sidebar categories."""

    main: NavTab | None = None
    manage_users: Tab | None = None
    manage_invites: Tab | None = None
    create_invite: Tab | None = None

    installed: SortedList[str] = field(default_factory=SortedList)


@dataclass
class _AppStoreComponents:
    """Used to store user-defined components."""

    main: ComponentType | None = None


@dataclass
class _AppStoreTabs:
    """Used to store NavTab/Tab objects for the default sidebar categories."""

    main: NavTab | None = None


@dataclass
class _ServerSettingsComponents:
    """Used to store user-defined components."""

    main: ComponentType | None = None
    general: ComponentType | None = None
    styling: ComponentType | None = None
    webserver: ComponentType | None = None
    email: ComponentType | None = None
    system_info: ComponentType | None = None


@dataclass
class _ServerSettingsTabs:
    """Used to store NavTab/Tab objects for the default sidebar categories."""

    main: NavTab | None = None
    general: Tab | None = None
    styling: Tab | None = None
    webserver: Tab | None = None
    email: Tab | None = None
    system_info: Tab | None = None
    licenses: Tab | None = None

    installed: SortedList[str] = field(default_factory=SortedList)


@dataclass
class ComponentConfig:
    homepage: ComponentType | None = None
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
    user_settings: _UserSettingsTabs = field(
        default_factory=_UserSettingsTabs,
    )
    sign_out: _SignOutTabs = field(
        default_factory=_SignOutTabs,
    )
    user_management: _UserManagementTabs = field(
        default_factory=_UserManagementTabs,
    )
    app_store: _AppStoreTabs = field(
        default_factory=_AppStoreTabs,
    )
    server_settings: _ServerSettingsTabs = field(
        default_factory=_ServerSettingsTabs,
    )


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
    default_nav_tab: NavTab | None = None
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
    admin_nav_tabs: list[NavTab] = field(default_factory=list)
    debug_nav_tabs: list[NavTab] = field(default_factory=list)
