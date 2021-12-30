from django.urls.base import reverse
from idom.core.vdom import make_vdom_constructor


iframe = make_vdom_constructor("iframe")


def performance(websocket, state, set_state):
    return iframe({"src": reverse("silk:summary")})


def health_check(websocket, state, set_state):
    return iframe({"src": reverse("health_check")})


def database(websocket, state, set_state):
    return iframe({"src": reverse("admin:index")})


def code_outline(websocket, state, set_state):
    return iframe({"src": reverse("django-admindocs-docroot")})


def api_docs(websocket, state, set_state):
    return iframe({"src": reverse("swagger_ui")})
