from dataclasses import dataclass, field
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
class ViewportSelector:
    initial: str = "initial"
    loading: str = "loading"
    primary: str = "primary"
    secondary: str = "secondary"


@dataclass
class Viewport:
    component: Callable
    selector: ViewportSelector = ViewportSelector.primary
    padding: bool = True


@dataclass
class NavTab:
    viewport: Viewport = None
    on_click: Callable = None


@dataclass
class ModalState:
    show: bool = False
    size: str = "lg"
    centered: bool = True
    kwargs: dict = field(default_factory=dict)


@dataclass
class HomepageState:
    page_title: str = "Loading..."
    viewport_selector: ViewportSelector = ViewportSelector.initial
    viewport_padding: bool = True
    viewport_primary: Callable = None
    viewport_secondary: Callable = None
    modal_state: ModalState = ModalState()
    modal: Callable = None


@dataclass
class TabbedViewportState:
    current_tab: Callable


@dataclass
class Seconds:
    minute: int = 60
    hour: int = minute * 60
    day: int = hour * 24
    week: int = day * 7
    month: int = week * 4
    year: int = month * 12
