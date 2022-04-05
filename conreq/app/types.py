from dataclasses import dataclass, field
from typing import Callable

from idom.core.types import VdomDict
from sortedcontainers import SortedSet


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
    html_class: str = ""
    padding: bool = True
    auth: AuthLevel = AuthLevel.user


@dataclass(order=True)
class NavTab:
    name: str
    viewport: Viewport = None
    on_click: Callable = None
    auth: AuthLevel = AuthLevel.user

    def __eq__(self, __o: object) -> bool:
        return _check_name(self, __o)


@dataclass(order=True)
class Tab:
    name: str
    component: Callable
    html_class: str = ""
    padding: bool = True
    on_click: Callable = None
    auth: AuthLevel = AuthLevel.user

    def __eq__(self, __o: object) -> bool:
        return _check_name(self, __o)


@dataclass(order=True)
class NavGroup:
    name: str
    icon: Icon = None
    tabs: SortedSet[NavTab] = field(default_factory=SortedSet)

    def __eq__(self, __o: object) -> bool:
        return _check_name(self, __o)


@dataclass
class ModalState:
    # TODO: Set as immutable and remove all copy() calls
    show: bool = False
    size: str = "lg"
    centered: bool = True
    kwargs: dict = field(default_factory=dict)


@dataclass
class HomepageState:
    # TODO: Set as immutable and remove all copy() calls
    page_title: str = "Loading..."
    viewport_selector: ViewportSelector = ViewportSelector.initial
    viewport_primary: Viewport = None
    viewport_secondary: Viewport = None
    modal_state: ModalState = ModalState()
    modal: Callable = None


@dataclass
class TabbedViewportState:
    current_tab: Tab


@dataclass
class Seconds:
    minute: int = 60
    hour: int = minute * 60
    day: int = hour * 24
    week: int = day * 7
    month: int = week * 4
    year: int = month * 12


def _check_name(self, __o):
    if isinstance(__o, str):
        return self.name.lower() == __o.lower()
    return self.name.lower() == __o.name.lower()
