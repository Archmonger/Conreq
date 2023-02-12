from conreq import config


def landing(template: str):
    """Changes the landing HTML template."""
    config.templates.landing = template


def home(template: str):
    """Changes the home HTML template."""
    config.templates.home = template


def sign_up(template: str):
    """Changes the sign up HTML template."""
    config.templates.sign_up = template


def sign_in(template: str):
    """Changes the sign in HTML template."""
    config.templates.sign_in = template


def password_reset(template: str):
    """Changes the password reset HTML template."""
    config.templates.password_reset = template


def password_reset_sent(template: str):
    """Changes the password reset HTML template."""
    config.templates.password_reset_sent = template


def password_reset_confirm(template: str):
    """Changes the password reset HTML template."""
    config.templates.password_reset_confirm = template


def offline(template: str):
    """Changes the offline HTML template."""
    config.templates.offline = template
