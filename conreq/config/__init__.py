from conreq.config.types import (
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
_internal_tabs = _InternalTabConfig()
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
    "_internal_tabs",
    "templates",
    "views",
    "wsgi",
]


def load_default_tabs():
    # pylint: disable=import-outside-toplevel, unused-import
    from conreq.config import default_tabs  # noqa: F401


load_default_tabs()
