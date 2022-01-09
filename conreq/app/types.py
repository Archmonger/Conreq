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
class ViewportState:
    initial: str = "initial"
    loading: str = "loading"
    primary: str = "primary"
    secondary: str = "secondary"


@dataclass
class ModalState:
    loading: str = "loading"
    hidden: str = "hidden"
    show: str = "show"


@dataclass
class HomepageState:
    page_title: str = "Loading..."
    viewport: ViewportState = ViewportState.initial
    viewport_padding: bool = True
    viewport_primary: Callable = None
    viewport_secondary: Callable = None
    modal: ModalState = ModalState.loading
    modal_title: str = "Loading..."
    modal_header: Callable = None
    modal_body: Callable = None
    modal_footer: Callable = None


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
