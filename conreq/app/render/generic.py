"""Helpers to render IDOM elements on the page"""
from conreq.app import AuthLevel, Icon, Navtab, Viewport

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable


def toast_message(
    title: str,
    message: str,
    icon: str,
    iziToast_params: dict = None,
):
    pass


def modal():
    pass


def viewport(
    selector: Viewport = Viewport.primary,
    auth_level: AuthLevel = AuthLevel.user,
    nav_tab: Navtab = None,
    group_icon: Icon = None,
    icon_left: Icon = None,
    icon_right: Icon = None,
):
    pass
