from dataclasses import dataclass


@dataclass
class AuthLevel:
    anonymous: int = 0
    user: int = 1
    admin: int = 2


@dataclass
class Viewport:
    loading: int = 0
    primary: int = 1
    secondary: int = 2


@dataclass
class Modal:
    loading: int = 0
    hidden: int = 1
    show: int = 2
