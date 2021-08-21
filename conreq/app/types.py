from dataclasses import dataclass


@dataclass
class AuthLevel:
    anonymous: int = 0
    user: int = 1
    admin: int = 2


@dataclass
class Viewport:
    primary: int = 0
    secondary: int = 1
