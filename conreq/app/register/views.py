from conreq import config
from conreq.utils.profiling import profiled_view

# pylint: disable=import-outside-toplevel


def landing(view):
    """Changes the home view."""
    config.views.landing = profiled_view(view)
    return view


def home(view):
    """Changes the home view."""
    config.views.home = profiled_view(view)
    return view


def sign_up(view):
    """Changes the sign up view."""
    config.views.sign_up = profiled_view(view)
    return view


def sign_in(view):
    """Changes the sign in view."""
    config.views.sign_in = profiled_view(view)
    return view


def edit_user(view):
    """Changes the delete user view."""
    config.views.edit_user = profiled_view(view)
    return view


def delete_user(view):
    """Changes the delete user view."""
    config.views.delete_user = profiled_view(view)
    return view


def password_reset(view):
    """Changes the password reset view."""
    config.views.password_reset = profiled_view(view)
    return view


def password_reset_sent(view):
    """Changes the password reset sent view."""
    config.views.password_reset_sent = profiled_view(view)
    return view


def password_reset_confirm(view):
    """Changes the password reset confirm view."""
    config.views.password_reset_confirm = profiled_view(view)
    return view


def offline(view):
    """Changes the offline view."""
    config.views.offline = profiled_view(view)
    return view


def service_worker(view):
    """Changes the service worker view."""
    config.views.service_worker = profiled_view(view)
    return view


def web_manifest(view):
    """Changes the web manifest view."""
    config.views.web_manifest = profiled_view(view)
    return view
