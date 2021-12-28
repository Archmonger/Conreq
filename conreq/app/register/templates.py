from conreq import config


def landing_template(template: str) -> None:
    """Changes the landing page variable."""
    config.templates.landing = template


def home_template(template: str) -> None:
    """Changes the home page variable."""
    config.templates.home = template


def sign_up_template(template: str) -> None:
    """Changes the sign up page variable."""
    config.templates.sign_up = template


def sign_in_template(template: str) -> None:
    """Changes the sign in page variable."""
    config.templates.sign_in = template


def password_reset_template(template: str) -> None:
    """Changes the password reset page variable."""
    config.templates.password_reset = template


def password_reset_sent_template(template: str) -> None:
    """Changes the password reset page variable."""
    config.templates.password_reset_sent = template


def password_reset_confirm_template(template: str) -> None:
    """Changes the password reset page variable."""
    config.templates.password_reset_confirm = template
