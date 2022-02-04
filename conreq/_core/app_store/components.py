from django.templatetags.static import static
from idom import component
from idom.html import div, h4, h5, i, link, p

from conreq import config
from conreq._core.utils import tab_constructor
from conreq.app import register


class PlaceholderApp:
    id = 0
    name = "Placeholder App"
    description = "This is a placeholder description. This will be removed in the future. Please pay no attention to this text. But what if the text gets too long? Who knows what will happen, but I can probably guess that it'll be great!"
    author = "Placeholder Author"
    version = "1.0.0"
    downloads = "0"
    category = "Placeholder Category"


@register.component.app_store()
@component
def app_store(websocket, state, set_state):
    # TODO: Update app store entries every first load
    # TODO: Remove this top level div later https://github.com/idom-team/idom/issues/538
    return div(
        link({"rel": "stylesheet", "href": static("conreq/app_store.css")}),
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


def spotlight(title, description, apps=None):
    # https://stackoverflow.com/questions/43547430/how-can-i-completely-hide-elements-that-overflow-their-container-vertically
    return div(
        {"className": "spotlight"},
        h4({"className": "title"}, title),
        p({"className": "description"}, description),
        div(
            {"className": "card-stage"},
            [card() for _ in range(8)],
        ),
        div({"className": "btn btn-sm btn-primary show-more"}, "SHOW MORE"),
    )


def card(app: PlaceholderApp = PlaceholderApp()):
    return div(
        {"className": "card"},
        div(
            {"className": "top"},
            div(
                {"className": "text-region"},
                h5({"className": "card-title"}, app.name),
                div({"className": "card-author"}, app.author),
                div({"className": "card-category"}, app.category),
            ),
            div({"className": "image"}),
        ),
        div(
            {"className": "btn-container"},
            div({"className": "btn btn-sm btn-secondary"}, "Info"),
            div({"className": "btn btn-sm btn-secondary"}, "Repo"),
            div({"className": "btn btn-sm btn-primary"}, "Install"),
        ),
        div({"className": "version"}, f"Version: {app.version}"),
        div({"className": "downloads"}, f"Downloads: {app.downloads}"),
        div({"className": "description"}, app.description),
        # TODO: Check if integer keys are broken in normal scenarios
        key=str(app.id),
    )


# pylint: disable=protected-access
config._homepage.admin_nav_tabs[1] = tab_constructor(
    "App Store", app_store, html_class="app-store"
)
