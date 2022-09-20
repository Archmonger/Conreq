from conreq import config


def manage_users():
    """Changes the manage users component."""

    def decorator(func):
        config.components.user_management = func
        return func

    return decorator


def user_invites():
    """Changes the manage users component."""

    def decorator(func):
        config.components.user_invites = func
        return func

    return decorator


def server_settings():
    """Changes the server settings component."""

    def decorator(func):
        config.components.server_settings = func
        return func

    return decorator


def user_settings():
    """Changes the user settings component."""

    def decorator(func):
        config.components.user_settings = func
        return func

    return decorator


def app_store():
    """Changes the app store component."""

    def decorator(func):
        config.components.app_store = func
        return func

    return decorator


def loading_animation():
    """Changes the default component loading animation."""

    def decorator(func):
        config.components.loading_animation = func
        return func

    return decorator
