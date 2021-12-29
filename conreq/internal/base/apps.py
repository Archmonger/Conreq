import idom
from channels.auth import logout
from django.apps import AppConfig
from django.urls.base import reverse
from idom.core.vdom import make_vdom_constructor
from idom.html import div, i, p

from conreq import config
from conreq.app import register
from conreq.utils.components import django_to_idom


class BaseConfig(AppConfig):
    name = "conreq.internal.base"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from django_idom import IDOM_WEBSOCKET_PATH

        config.asgi.websockets.append(IDOM_WEBSOCKET_PATH)

        # TODO: Move this navbar registration stuff somewhere else later
        # pylint: disable=unused-argument
        register.homepage.nav_group("User", i({"className": "fas fa-users icon-left"}))
        register.homepage.nav_group("Admin", i({"className": "fas fa-cogs icon-left"}))
        register.homepage.nav_group(
            "Debug", i({"className": "fas fa-spider icon-left"})
        )

        from conreq.internal.user_settings.views import user_settings

        register.homepage.nav_tab("Settings", "User")(user_settings)

        @register.homepage.nav_tab("Sign Out", "User")
        @idom.component
        def sign_out(websocket, state, set_state):
            @idom.hooks.use_effect
            async def logout_user():
                await logout(websocket.scope)

            return div()

        from conreq.internal.manage_users.views import manage_users

        register.homepage.nav_tab("Manage Users", "Admin")(
            django_to_idom()(manage_users)
        )

        @register.homepage.nav_tab("App Store", "Admin")
        def app_store(websocket, state, set_state):
            return p("This is a temporary stub for the app store tab.")

        from conreq.internal.server_settings.views import server_settings

        register.homepage.nav_tab("Server Settings", "Admin")(
            django_to_idom()(server_settings)
        )

        iframe = make_vdom_constructor("iframe")

        @register.homepage.nav_tab("Performance", "Debug", padding=False)
        def performance(websocket, state, set_state):
            return iframe({"src": reverse("silk:summary")})

        @register.homepage.nav_tab("Health Check", "Debug", padding=False)
        def health_check(websocket, state, set_state):
            return iframe({"src": reverse("health_check")})

        @register.homepage.nav_tab("Database", "Debug", padding=False)
        def database(websocket, state, set_state):
            return iframe({"src": reverse("admin:index")})

        @register.homepage.nav_tab("Code Outline", "Debug", padding=False)
        def code_outline(websocket, state, set_state):
            return iframe({"src": reverse("django-admindocs-docroot")})

        @register.homepage.nav_tab("API Docs", "Debug", padding=False)
        def api_docs(websocket, state, set_state):
            return iframe({"src": reverse("swagger_ui")})
