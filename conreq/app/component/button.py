from dataclasses import dataclass
from typing import Callable, Optional

from .icon import Icon


@dataclass
class GenericButton:
    text: str
    icon: Optional[Icon] = None
    font_color: Optional[str] = "#FFF"
    background_color: Optional[str] = "var(--accent-color)"
    click_action: Optional[Callable] = None  # Will be an IDOM event
