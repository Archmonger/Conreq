from dataclasses import dataclass


@dataclass
class AuthLevel:
    anonymous: int = "anonymous"
    user: int = "user"
    admin: int = "admin"


@dataclass
class Viewport:
    loading: int = "loading"
    primary: int = "primary"
    secondary: int = "secondary"


@dataclass
class Modal:
    loading: int = "loading"
    hidden: int = "hidden"
    show: int = "show"
