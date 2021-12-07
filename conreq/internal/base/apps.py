import idom
from channels.auth import logout
from django.apps import AppConfig
from django.urls.base import reverse
from idom.core.vdom import make_vdom_constructor
from idom.html import div, i, p

import conreq
from conreq.app import register
from conreq.app.selectors import Viewport


class BaseConfig(AppConfig):
    name = "conreq.internal.base"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from django_idom import IDOM_WEBSOCKET_PATH

        conreq.config.websockets.append(IDOM_WEBSOCKET_PATH)

        # TODO: Move this navbar registration stuff somewhere else later
        # pylint: disable=unused-argument
        register.nav_group("User", i({"className": "fas fa-users icon-left"}))
        register.nav_group("Admin", i({"className": "fas fa-cogs icon-left"}))
        register.nav_group("Debug", i({"className": "fas fa-spider icon-left"}))

        @register.nav_tab("Settings", "User")
        def settings(websocket, state, set_state):
            return p("settings")

        @register.nav_tab("Sign Out", "User")
        @idom.component
        def sign_out(websocket, state, set_state):
            @idom.hooks.use_effect
            async def logout_user():
                await logout(websocket.scope)

            return div()

        @register.nav_tab("Manage Users", "Admin")
        def manage_users(websocket, state, set_state, viewport=Viewport.secondary):
            return p("manage users")

        @register.nav_tab("App Store", "Admin")
        def app_store(websocket, state, set_state):
            return p("app store")

        @register.nav_tab("Server Settings", "Admin")
        def system_settings(websocket, state, set_state):
            return p("server settings")

        iframe = make_vdom_constructor("iframe")

        @register.nav_tab("Performance", "Debug", padding=False)
        def performance(websocket, state, set_state):
            return iframe({"src": reverse("silk:summary")})

        @register.nav_tab(
            "Database", "Debug", padding=False, viewport=Viewport.secondary
        )
        def database(websocket, state, set_state):
            return iframe({"src": reverse("admin:index")})

        @register.nav_tab("Code Outline", "Debug", padding=False)
        def code_outline(websocket, state, set_state):
            return iframe({"src": reverse("django-admindocs-docroot")})

        @register.nav_tab("API Docs", "Debug", padding=False)
        def api_docs(websocket, state, set_state):
            return iframe({"src": reverse("swagger_ui")})
