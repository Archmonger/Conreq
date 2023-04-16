from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Sequence

from reactpy.core.component import Component
from reactpy.core.hooks import Context, create_context
from reactpy.core.types import ComponentConstructor, VdomDict
from sortedcontainers import SortedSet

if TYPE_CHECKING:
    from reactpy_django.types import Connection

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
    component: ComponentConstructor | Callable[..., Component] | Callable[..., VdomDict]
    """The component to render in the viewport."""

    args: tuple = field(default_factory=tuple)
    """The arguments to pass to the viewport component."""

    html_class: str = ""
    """HTML class to apply to the viewport."""

    padding: bool = True
    """Whether or not to apply padding to the viewport."""

    page_title: str | None = None
    """The page title to display on the browser tab."""

    background: str | None = None  # TODO: Implement this
    """The background property to apply to the webpage."""


@dataclass(frozen=True)
class SidebarTab:
    name: str
    viewport: Viewport | None = None
    on_click: Callable[[SidebarTabEvent], None] | None = None
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
    component: ComponentConstructor | Callable[..., Component] | Callable[..., VdomDict]
    html_class: str = ""
    padding: bool = True
    on_click: Callable[[SubTabEvent], None] | None = None
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
    attributes: dict[str, str | None] | None = None
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
    # FIXME: Redo this when ReactPy supports react-bootstrap
    # https://github.com/reactive-python/reactpy/issues/786

    set_state: SetModalState = lambda _: None
    """A function that can be used to set this state."""

    show: bool = False
    """A toggle to set the modal's visibility."""

    modal_intent: ComponentConstructor | None = None
    """The modal that needs to be loaded."""

    modal_args: Sequence = field(default_factory=list)
    """The arguments to pass to the modal component."""

    modal_kwargs: dict = field(default_factory=dict)
    """The keyword arguments to pass to the modal component."""

    _modal: ComponentConstructor | None = None
    """The currently visible modal."""

    def reset_modal(self) -> None:
        """Resets the modal to defaults."""
        self.show = False
        self.modal_intent = None
        self._modal = None
        self.modal_args = []
        self.modal_kwargs = {}


SetModalState = Callable[[ModalState], None]
ModalStateContext: Context[ModalState] = create_context(ModalState())


@dataclass
class HomepageState:
    set_state: SetHomepageState = lambda _: None
    """A function that can be used to set this state."""

    viewport_loading: bool = False
    """A toggle to manually set the viewport loading state. This is only used
    by user defined viewport components."""

    viewport_intent: Viewport | None = None
    """The viewport that needs to be loaded."""

    _viewport: Viewport | None = None
    """The currently visible viewport."""


SetHomepageState = Callable[[HomepageState], None]
HomepageStateContext: Context[HomepageState] = create_context(HomepageState())


@dataclass
class AppStoreState:
    set_state: SetAppStoreState = lambda _: None
    """A function that can be used to set this state."""

    tab: Any | None = None
    """The current app store tab being rendered."""


SetAppStoreState = Callable[[AppStoreState], None]
AppStoreStateContext: Context[AppStoreState] = create_context(AppStoreState())


@dataclass
class TabbedViewportState:
    tab: SubTab | None
    """The current subtab being rendered."""

    set_state: SetTabbedViewportState = lambda _: None
    """A function that can be used to set this state."""


SetTabbedViewportState = Callable[[TabbedViewportState], None]
TabbedViewportStateContext: Context[TabbedViewportState] = create_context(
    TabbedViewportState(None)
)


@dataclass
class SidebarTabEvent:
    event: dict
    tab: SidebarTab
    connection: Connection
    homepage_state: HomepageState


@dataclass
class SubTabEvent:
    event: dict
    tab: SubTab
    connection: Connection
    homepage_state: HomepageState
    tabbed_viewport_state: TabbedViewportState


def _compare_names(self, __o):
    if isinstance(__o, str):
        return self.name.lower() == __o.lower()
    return self.name.lower() == __o.name.lower()
