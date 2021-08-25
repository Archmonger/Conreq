from dataclasses import dataclass
from typing import Callable

from .button import GenericButton


@dataclass
class GenericModal:
    title: str
    body: Callable  # Will be an IDOM component
    footer_buttons: list[GenericButton]


@dataclass
class CustomModal:
    """Modal with no header, body, or footer. User must design those himself."""

    modal: Callable  # Will be an IDOM component
