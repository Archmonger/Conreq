"""Conreq's configuration values."""

from dataclasses import dataclass


@dataclass
class Config:
    # Startup
    pre_run = []
    pre_startup = []
    setting_scripts = []
    installed_apps = []
    middleware = []
    landing_template = ""
    landing_view = None
    home_template = ""
    home_view = None
    sign_up_template = ""
    sign_up_view = None
    sign_in_template = ""
    sign_in_view = None
    password_reset_template = ""
    password_reset_view = None
    manage_users_component = None

    # ASGI
    websockets = []

    # WSGI
    api_endpoints = []
    url_patterns = []

    # Components
    navtabs = []
    server_setting_tabs = []
    user_setting_components = []

    # HTML Head
    css = []
    scss = []
    javascript = []
    fonts = []
    head_content = []
