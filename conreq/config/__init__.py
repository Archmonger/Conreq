from .configuration import (
    AsgiConfig,
    ComponentConfig,
    HomepageConfig,
    StartupConfig,
    TabConfig,
    TemplateConfig,
    ViewConfig,
    WsgiConfig,
)

asgi = AsgiConfig()
components = ComponentConfig()
homepage = HomepageConfig()
startup = StartupConfig()
tabs = TabConfig()
templates = TemplateConfig()
views = ViewConfig()
wsgi = WsgiConfig()

__all__ = [
    "asgi",
    "components",
    "homepage",
    "startup",
    "tabs",
    "templates",
    "views",
    "wsgi",
]
