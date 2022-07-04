from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

from idom.core.types import VdomDict
from sortedcontainers import SortedSet

# pylint: disable=protected-access


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
    _initial: str = "initial"
    """Used internally by Conreq to denote the first page load."""
    primary: str = "primary"
    """Selection of the primary viewport."""
    secondary: str = "secondary"
    """Selection of the secondary viewport."""
    auto: str = "auto"
    """Automatically select the viewport based on the current viewport selector."""


@dataclass
class Viewport:
    component: Callable
    selector: str = ViewportSelector.auto
    html_class: str = ""
    padding: bool = True
    auth: str = AuthLevel.user
    page_title: str | None = None
    expires: bool = True
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(order=True)
class NavTab:
    name: str
    viewport: Viewport | None = None
    on_click: Callable | None = None
    auth: str = AuthLevel.user

    def __eq__(self, __o: object) -> bool:
        return _compare_names(self, __o)


@dataclass(order=True)
class Tab:
    name: str
    component: Callable
    html_class: str = ""
    padding: bool = True
    on_click: Callable | None = None
    auth: str = AuthLevel.user

    def __eq__(self, __o: object) -> bool:
        return _compare_names(self, __o)


@dataclass(order=True)
class NavGroup:
    name: str
    icon: Icon | None = None
    tabs: SortedSet[NavTab] = field(default_factory=SortedSet)

    def __eq__(self, __o: object) -> bool:
        return _compare_names(self, __o)


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
    _viewport_intent: Viewport | None = None
    """The viewport that needs to be loaded."""
    _viewport_selector: str = ViewportSelector._initial
    """The currently visible viewport."""
    _viewport_primary: Viewport | None = None
    _viewport_secondary: Viewport | None = None

    _modal_intent: Callable | None = None
    """The modal that needs to be loaded."""
    _modal: Callable | None = None
    """The currently visible modal."""
    _modal_state: ModalState = ModalState()

    def set_viewport(self, viewport: Viewport):
        self._viewport_intent = viewport

    def set_modal(self, modal: Callable):
        self._modal_intent = modal


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


def _compare_names(self, __o):
    if isinstance(__o, str):
        return self.name.lower() == __o.lower()
    return self.name.lower() == __o.name.lower()
