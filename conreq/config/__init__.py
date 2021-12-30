from .configuration import (
    AsgiConfig,
    ComponentConfig,
    HomepageConfig,
    StartupConfig,
    TabConfig,
    TemplateConfig,
    ViewConfig,
    WsgiConfig,
    _InternalTabConfig,
)

asgi = AsgiConfig()
components = ComponentConfig()
homepage = HomepageConfig()
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
    "startup",
    "tabs",
    "_tabs",
    "templates",
    "views",
    "wsgi",
]
