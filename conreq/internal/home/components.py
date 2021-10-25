import idom
from idom.html import a, div, i, nav, h1

SIDEBAR = {
    "id": "sidebar",
    "class": "sidebar no-hightlighting collapsed",
    "data-aos": "fade-right",
    "data-aos-duration": "1000",
}
SIDEBAR_USER = {"class": "sidebar-user clickable"}
USER_PIC = {"class": "sidebar-profile-pic"}
USER_PIC_PLACEHOLDER = {"class": "fas fa-user"}
USERNAME = {"class": "username"}
ELLIPSIS = {"class": "ellipsis"}
NAVPAGES = {"id": "navpage", "class": "navpages"}
NAVGROUP = {
    "class": "nav-group clickable",
    "data-bs-toggle": "collapse",
    "data-bs-target": "#user-tabs",
    "aria-expanded": "true",
    "aria-controls": "user-tabs",
}
GROUP_NAME = {"class": "group-name ellipsis"}
GROUP_ICON = {"class": "group-icon"}
EXAMPLE_GROUP_ICON = {"class": "fas fa-user icon-left"}
GROUP_CARET = {"class": "fas fa-caret-up icon-right", "title": "Collapse group"}
TABS_COLLAPSE = {"id": "user-tabs", "class": "tabs-collapse collapse show"}
TABS_INDICATOR = {"class": "tabs-indicator"}
TABS = {"class": "tabs"}
NAV_TAB = {"class": "nav-tab"}


@idom.component
def hello(websocket):
    return h1("Hello World!")


@idom.component
def sidebar(websocket):
    return nav(
        SIDEBAR,
        div(
            SIDEBAR_USER,
            div(USER_PIC, i(USER_PIC_PLACEHOLDER)),
            div(USERNAME, div(ELLIPSIS, websocket.scope["user"].get_username())),
        ),
        div(
            NAVPAGES,
            div(
                NAVGROUP,
                div(
                    GROUP_NAME,
                    div(GROUP_ICON, i(EXAMPLE_GROUP_ICON)),
                    "This is an example sidebar group name!",
                ),
                i(GROUP_CARET),
            ),
            div(
                TABS_COLLAPSE,
                div(TABS_INDICATOR),
                div(
                    TABS,
                    div(NAV_TAB, a(ELLIPSIS, "Example Tab Name")),
                    div(NAV_TAB, a(ELLIPSIS, "Example Tab Name 2")),
                ),
            ),
        ),
    )
