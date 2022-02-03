from idom import component
from idom.html import div, h2, h5

from conreq import config
from conreq._core.utils import tab_constructor
from conreq.app import register


@register.component.app_store()
@component
def app_store(websocket, state, set_state):
    # TODO: Update app store entries every first load
    # TODO: Remove this top level div
    return div(
        recently_added(),
        recently_updated(),
        most_popular(),
        top_downloaded(),
        our_favorites(),
        essentials(),
        random_selection(),
    )


def recently_added():
    return spotlight("Recently Added", "The latest from our community.")


def recently_updated():
    return spotlight("Recently Updated", "Actively maintained for all to enjoy.")


def most_popular():
    return spotlight("Most Popular", "These have gained a serious amount lot of love.")


def top_downloaded():
    return spotlight("Top Downloaded", "Tons of downloads!")


def our_favorites():
    return spotlight("Our Favorites", "A curated list of our favorites.")


def essentials():
    return spotlight("Essentials", "Something we think all users should consider.")


def random_selection():
    return spotlight("Random Selection", "Are you feeling lucky today?")


def spotlight(title, description, all_apps=None, spotlight_apps=None):
    # TODO: Spotlight will contain at most 6 apps. Hide elements that don't fit.
    # https://stackoverflow.com/questions/43547430/how-can-i-completely-hide-elements-that-overflow-their-container-vertically
    return div(
        h2(title),
        h5(description + " SHOW MORE"),
        div(">> APPS GO HERE <<"),
    )


# pylint: disable=protected-access
config._homepage.admin_nav_tabs[1] = tab_constructor("App Store", app_store)
