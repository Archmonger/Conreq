from dataclasses import dataclass
from typing import Callable

from idom.core.proto import VdomDict


class Icon(VdomDict):
    pass


@dataclass
class ViewType:
    view: str = "django"
    component: str = "idom"


@dataclass
class AuthLevel:
    anonymous: str = "anonymous"
    user: str = "user"
    admin: str = "admin"


@dataclass
class Viewport:
    initial: str = "initial"
    loading: str = "loading"
    primary: str = "primary"
    secondary: str = "secondary"


@dataclass
class Modal:
    loading: str = "loading"
    hidden: str = "hidden"
    show: str = "show"


@dataclass
class HomepageState:
    page_title: str = "Loading..."
    viewport: Viewport = Viewport.initial
    viewport_padding: bool = True
    viewport_primary: Callable = None
    viewport_secondary: Callable = None
    modal: Modal = Modal.loading
    modal_title: str = "Loading..."
    modal_header: Callable = None
    modal_body: Callable = None
    modal_footer: Callable = None


@dataclass
class TabbedViewportState:
    current_tab: Callable
