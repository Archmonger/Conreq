"""Conreq's configuration values."""

from dataclasses import dataclass, field
from typing import Callable

from django.views import View
from idom.core.component import Component
from idom.html import div, span
from idom.types import VdomDict
from sortedcontainers import SortedList

from conreq.types import CSS, SCSS, HTMLTemplate, JavaScript, SidebarTab, SubTab

# pylint: disable=too-many-instance-attributes


# Component Configuration


@dataclass
class _UserSettingsComponents:
    """Used to store user-defined components."""

    main: Component | None = None
    general: Component | None = None
    change_password: Component | None = None
    delete_account: Component | None = None


@dataclass
class _SignOutComponents:
    """Used to store user-defined components."""

    main: Component | None = None
    event: Callable | None = None


@dataclass
class _UserManagementComponents:
    """Used to store user-defined components."""

    main: Component | None = None
    manage_users: Component | None = None
    edit_user: Component | None = None
    delete_user: Component | None = None
    manage_invites: Component | None = None
    create_invite: Component | None = None


@dataclass
class _ServerSettingsComponents:
    """Used to store user-defined components."""

    main: Component | None = None
    general: Component | None = None
    styling: Component | None = None
    webserver: Component | None = None
    email: Component | None = None
    system_info: Component | None = None


@dataclass
class _LoadingAnimationComponents:
    """Used to store user-defined components."""

    large: VdomDict = field(
        default_factory=lambda: div(
            {"className": "spinner-border loading-animation lg", "role": "status"},
            span({"className": "sr-only"}, "Loading..."),
        ),
    )
    small: Component | VdomDict = field(
        default_factory=lambda: div(
            {"className": "spinner-border loading-animation", "role": "status"},
            span({"className": "sr-only"}, "Loading..."),
        ),
    )


@dataclass
class _AppStoreComponents:
    """Used to store user-defined components."""

    main: Component | None = None


# Tab Configuration


@dataclass
class _UserSettingsTabs:
    """Used to store NavTab/Tab objects for the default sidebar categories."""

    main: SidebarTab | None = None
    general: SubTab | None = None
    change_password: SubTab | None = None
    delete_account: SubTab | None = None

    installed: SortedList = field(default_factory=SortedList)


@dataclass
class _SignOutTabs:
    """Used to store NavTab/Tab objects for the default sidebar categories."""

    main: SidebarTab | None = None


@dataclass
class _UserManagementTabs:
    """Used to store NavTab/Tab objects for the default sidebar categories."""

    main: SidebarTab | None = None
    manage_users: SubTab | None = None
    manage_invites: SubTab | None = None
    create_invite: SubTab | None = None

    installed: SortedList = field(default_factory=SortedList)


@dataclass
class _AppStoreTabs:
    """Used to store NavTab/Tab objects for the default sidebar categories."""

    main: SidebarTab | None = None


@dataclass
class _ServerSettingsTabs:
    """Used to store NavTab/Tab objects for the default sidebar categories."""

    main: SidebarTab | None = None
    general: SubTab | None = None
    styling: SubTab | None = None
    webserver: SubTab | None = None
    email: SubTab | None = None
    system_info: SubTab | None = None
    licenses: SubTab | None = None

    installed: SortedList = field(default_factory=SortedList)


# Top level configuration


@dataclass
class StartupConfig:
    setting_scripts: set[str] = field(default_factory=set)
    # TODO: Implement pre_run scripts
    pre_run: set[Callable] = field(default_factory=set)
    processes: set[Callable] = field(default_factory=set)


@dataclass
class ViewConfig:
    landing: Callable | View | None = None
    home: Callable | View | None = None
    sign_up: Callable | View | None = None
    sign_in: Callable | View | None = None
    edit_user: Callable | View | None = None
    delete_user: Callable | View | None = None
    password_reset: Callable | View | None = None
    password_reset_sent: Callable | View | None = None
    password_reset_confirm: Callable | View | None = None
    offline: Callable | View | None = None
    service_worker: Callable | View | None = None
    web_manifest: Callable | View | None = None


@dataclass
class TemplateConfig:
    # FIXME: Some of these don't respect the settings change
    landing: str = ""
    home: str = "conreq/home.html"
    sign_up: str = "conreq/sign_up.html"
    sign_in: str = "conreq/sign_in.html"
    edit_user: str = "conreq/form.html"
    delete_user: str = "conreq/delete_confirm.html"
    password_reset: str = "conreq/password_reset.html"
    password_reset_sent: str = "conreq/password_reset_sent.html"
    password_reset_confirm: str = "conreq/password_reset_confirm.html"
    offline: str = "conreq/offline.html"


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
    loading_animation: _LoadingAnimationComponents = field(
        default_factory=_LoadingAnimationComponents
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
    user_settings_top: list[SubTab] = field(default_factory=list)
    user_settings_bottom: list[SubTab] = field(default_factory=list)
    user_management: list[SubTab] = field(default_factory=list)
    server_settings: list[SubTab] = field(default_factory=list)


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
    sidebar_tabs: SortedList = field(default_factory=SortedList)
    default_sidebar_tab: SidebarTab | None = None
    # TODO: Implement CSS and JS registration
    local_stylesheets: list[CSS] = field(default_factory=list)
    remote_stylesheets: list[CSS] = field(default_factory=list)
    scss_stylesheets: list[SCSS] = field(default_factory=list)
    local_scripts: list[JavaScript] = field(default_factory=list)
    remote_scripts: list[JavaScript] = field(default_factory=list)
    head_content: list[HTMLTemplate] = field(default_factory=list)


@dataclass
class _InternalHomepageConfig:
    user_sidebar_tabs: list[SidebarTab] = field(default_factory=list)
    admin_sidebar_tabs: list[SidebarTab] = field(default_factory=list)
    debug_sidebar_tabs: list[SidebarTab] = field(default_factory=list)
