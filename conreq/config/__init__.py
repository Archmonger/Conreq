from .configuration import (
    AsgiConfig,
    ComponentConfig,
    HomepageConfig,
    StartupConfig,
    TabConfig,
    TemplateConfig,
    ViewConfig,
    WsgiConfig,
    _InternalHomepageConfig,
    _InternalTabConfig,
)

asgi = AsgiConfig()
components = ComponentConfig()
homepage = HomepageConfig()
_homepage = _InternalHomepageConfig()
startup = StartupConfig()
tabs = TabConfig()
_tabs = _InternalTabConfig()
templates = TemplateConfig()
views = ViewConfig()
wsgi = WsgiConfig()

__all__ = [
    "asgi",
    "components",
    "homepage",
    "_homepage",
    "startup",
    "tabs",
    "_tabs",
    "templates",
    "views",
    "wsgi",
]
