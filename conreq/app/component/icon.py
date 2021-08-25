from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Icon:
    html_tag: Optional[str]
    classes: Optional[str]
    text: Optional[str]
    click_action: Optional[Callable] = None
