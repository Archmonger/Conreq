from dataclasses import dataclass
from typing import Callable

from conreq.app.selectors import Modal, Viewport


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
