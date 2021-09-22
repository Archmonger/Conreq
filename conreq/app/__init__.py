from conreq.app.configuration import _Config

from . import component, register, render, selectors

__all__ = ["component", "register", "render", "selectors"]

config: _Config = _Config()
