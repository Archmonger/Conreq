from dataclasses import dataclass


@dataclass
class ViewType:
    view: str = "django"
    component: str = "idom"


@dataclass
class AuthLevel:
    anonymous: str = "anonymous"
    user: str = "user"
    admin: str = "admin"


@dataclass
class Viewport:
    initial: str = "initial"
    loading: str = "loading"
    primary: str = "primary"
    secondary: str = "secondary"


@dataclass
class Modal:
    loading: str = "loading"
    hidden: str = "hidden"
    show: str = "show"
