# TODO: Create generics


def app(path: str):
    pass


def websocket(consumer, path: str, regex: bool = False):
    pass


def url(path: str, regex: bool = False):
    pass


def nav_tab(
    page_name: str,
    group_name: str,
    auth_level: int = 1,
    group_icon_cls: str = None,
    group_icon_txt: str = None,
    icon_left_cls: str = None,
    icon_left_txt: str = None,
    icon_right_cls: str = None,
    icon_right_txt: str = None,
):
    pass


def api(path: str, version: int, regex: bool = False):
    pass


def server_settings(page_name: str):
    pass


def user_settings(admin_only: bool = False):
    pass


def middleware(position_to: str = None, position_after: bool = True):
    pass


def component():
    pass
