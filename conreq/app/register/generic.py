from channels.consumer import AsyncConsumer

from conreq.app import AuthLevel, Icon, Navtab, Viewport

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable


def websocket(consumer: AsyncConsumer, path: str, regex: bool = False):
    pass


def url(path: str, regex: bool = False):
    pass


def navtab(
    selector: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
    nav_tab: Navtab = None,
    group_icon: Icon = None,
    icon_left: Icon = None,
    icon_right: Icon = None,
):
    pass


def api(path: str, version: int, auth: bool = True, regex: bool = False):
    pass


def server_settings(page_name: str):
    pass


def user_settings(admin_only: bool = False):
    pass
