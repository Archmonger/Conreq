import conreq


def landing_template(template: str) -> None:
    """Changes the landing page variable."""
    conreq.config.landing_template = template


def home_template(template: str) -> None:
    """Changes the home page variable."""
    conreq.config.home_template = template


def sign_up_template(template: str) -> None:
    """Changes the sign up page variable."""
    conreq.config.sign_up_template = template


def sign_in_template(template: str) -> None:
    """Changes the sign in page variable."""
    conreq.config.sign_in_template = template


def password_reset_template(template: str) -> None:
    """Changes the password reset page variable."""
    conreq.config.password_reset_template = template


def loading_animation_template(template: str) -> None:
    """Changes the loading animation template variable."""
    conreq.config.loading_animation_template = template
