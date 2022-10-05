from dataclasses import dataclass, field
from typing import Any, Callable

from idom.core.component import Component
from idom.core.types import VdomDict
from sortedcontainers import SortedSet

# pylint: disable=protected-access


class Icon(VdomDict):
    pass


@dataclass(frozen=True)
class Seconds:
    minute: int = 60
    hour: int = minute * 60
    day: int = hour * 24
    week: int = day * 7
    month: int = week * 4
    year: int = month * 12


@dataclass(frozen=True)
class AuthLevel:
    anonymous: str = "anonymous"
    user: str = "user"
    admin: str = "admin"


@dataclass
class Viewport:
    component: Component
    html_class: str = ""
    padding: bool = True
    page_title: str | None = None
    background: str | None = None  # TODO: Implement this


@dataclass(order=True)
class SidebarTab:
    name: str
    viewport: Viewport | None = None
    on_click: Callable[["SidebarTabEvent"], None] | None = None
    auth: str = AuthLevel.user

    def __eq__(self, __o: object) -> bool:
        return _compare_names(self, __o)


@dataclass(order=True)
class SubTab:
    name: str
    component: Component
    html_class: str = ""
    padding: bool = True
    on_click: Callable[["SubTabEvent"], None] | None = None
    auth: str = AuthLevel.user

    def __eq__(self, __o: object) -> bool:
        return _compare_names(self, __o)


@dataclass(order=True)
class NavGroup:
    name: str
    icon: Icon | None = None
    tabs: SortedSet = field(default_factory=SortedSet)

    def __eq__(self, __o: object) -> bool:
        return _compare_names(self, __o)


@dataclass
class FileLink:
    path: str
    attributes: dict[str, str | int] | None = None
    local: bool = True


class CSS(FileLink):
    ...


class JavaScript(FileLink):
    ...


@dataclass
class SCSS:
    path: str
    attributes: dict | None = None


@dataclass
class HTMLTemplate:
    path: str


@dataclass
class ModalState:
    _show: bool = False
    # FIXME: Some options are not available until IDOM supports react-bootstrap
    # Solution: https://github.com/idom-team/idom/issues/786

    # _size: str = "lg"
    # _centered: bool = True
    # _kwargs: dict = field(default_factory=dict)

    def set_show(self, show: bool):
        self._show = show

    # def set_size(self, size: str):
    #     self._size = size

    # def set_centered(self, centered: bool):
    #     self._centered = centered

    # def set_kwargs(self, kwargs: dict):
    #     self._kwargs = kwargs


@dataclass
class HomepageState:
    _viewport_intent: Viewport | None = None
    """The viewport that needs to be loaded."""
    """The currently visible viewport."""
    _viewport: Viewport | None = None

    _modal_intent: Callable | None = None
    """The modal that needs to be loaded."""
    _modal: Callable | None = None
    """The currently visible modal."""
    modal_state: ModalState = ModalState()

    def set_viewport(self, viewport: Viewport):
        self._viewport_intent = viewport

    def set_modal(self, modal: Callable):
        self._modal_intent = modal


@dataclass
class TabbedViewportState:
    _tab: SubTab | None

    def set_tab(self, tab: SubTab):
        self._tab = tab


@dataclass
class SidebarTabEvent:
    event: dict
    tab: SidebarTab
    websocket: Any
    homepage_state: HomepageState
    set_homepage_state: Callable


@dataclass
class SubTabEvent:
    event: dict
    tab: SubTab
    websocket: Any
    homepage_state: HomepageState
    set_homepage_state: Callable
    tabbed_viewport_state: TabbedViewportState
    set_tabbed_viewport_state: Callable


def _compare_names(self, __o):
    if isinstance(__o, str):
        return self.name.lower() == __o.lower()
    return self.name.lower() == __o.name.lower()
