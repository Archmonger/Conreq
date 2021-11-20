from dataclasses import dataclass


@dataclass
class AuthLevel:
    anonymous: str = "anonymous"
    user: str = "user"
    admin: str = "admin"


@dataclass
class Viewport:
    loading: str = "loading"
    primary: str = "primary"
    secondary: str = "secondary"


@dataclass
class Modal:
    loading: str = "loading"
    hidden: str = "hidden"
    show: str = "show"
