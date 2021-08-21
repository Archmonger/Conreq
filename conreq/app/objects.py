"""Generic class types used to extend Conreq."""
from dataclasses import dataclass
from typing import Optional, Callable


@dataclass
class Icon:
    html_tag: Optional[str]
    classes: Optional[str]
    text: Optional[str]
    click_action: Optional[Callable] = None  # Will be an IDOM event (?)


@dataclass
class Navtab:
    page_name: str
    group_name: str


@dataclass
class ModalFooterButton:
    text: str
    icon: Optional[Icon] = None
    font_color: Optional[str] = "#FFF"
    background_color: Optional[str] = "var(--accent-color)"
    click_action: Optional[Callable] = None  # Will be an IDOM event (?)


@dataclass
class GenericModal:
    title: str
    body: Callable  # Will be an IDOM component
    footer_buttons: list[ModalFooterButton]


@dataclass
class CustomModal:
    """Modal with no header, body, or footer. User must design those himself."""

    modal: Callable  # Will be an IDOM component
