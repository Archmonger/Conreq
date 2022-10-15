from dataclasses import dataclass, field
from typing import Any, Callable

from idom.core.component import Component
from idom.core.types import VdomDict
from sortedcontainers import SortedSet

# pylint: disable=protected-access, too-few-public-methods


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


@dataclass(frozen=True)
class Viewport:
    component: Component
    html_class: str = ""
    padding: bool = True
    page_title: str | None = None
    background: str | None = None  # TODO: Implement this


@dataclass(frozen=True)
class SidebarTab:
    name: str
    viewport: Viewport | None = None
    on_click: Callable[["SidebarTabEvent"], None] | None = None
    auth: str = AuthLevel.user

    def __eq__(self, __o: object) -> bool:
        return _compare_names(self, __o)

    def __lt__(self, __o: object) -> bool:
        return self.name < getattr(__o, "name", "")

    def __gt__(self, __o: object) -> bool:
        return self.name > getattr(__o, "name", "")


@dataclass(frozen=True)
class SubTab:
    name: str
    component: Component
    html_class: str = ""
    padding: bool = True
    on_click: Callable[["SubTabEvent"], None] | None = None
    auth: str = AuthLevel.user

    def __eq__(self, __o: object) -> bool:
        return _compare_names(self, __o)

    def __lt__(self, __o: object) -> bool:
        return self.name < getattr(__o, "name", "")

    def __gt__(self, __o: object) -> bool:
        return self.name > getattr(__o, "name", "")


@dataclass(frozen=True)
class NavGroup:
    name: str
    icon: Icon | None = None
    tabs: SortedSet = field(default_factory=SortedSet)

    def __eq__(self, __o: object) -> bool:
        return _compare_names(self, __o)

    def __lt__(self, __o: object) -> bool:
        return self.name < getattr(__o, "name", "")

    def __gt__(self, __o: object) -> bool:
        return self.name > getattr(__o, "name", "")


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
    # FIXME: Some options are not available until IDOM supports react-bootstrap
    # Solution: https://github.com/idom-team/idom/issues/786

    show: bool = False
    # size: str = "lg"
    # centered: bool = True
    # kwargs: dict = field(default_factory=dict)


@dataclass
class HomepageState:
    viewport_loading: bool = False
    """A toggle to manually set the viewport loading state. This is only used
    by user defined viewport components."""

    viewport_intent: Viewport | None = None
    """The viewport that needs to be loaded."""

    _viewport: Viewport | None = None
    """The currently visible viewport."""

    modal_intent: Callable | None = None
    """The modal that needs to be loaded."""

    _modal: Callable | None = None
    """The currently visible modal."""

    modal_state: ModalState = field(default_factory=ModalState)
    """The modal's current state object."""


@dataclass
class TabbedViewportState:
    tab: SubTab | None


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
