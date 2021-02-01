import secrets

from channels.auth import AnonymousUser, login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from conreq.apps.server_settings.models import ConreqConfig
from conreq.utils import log
from django.core.exceptions import ValidationError
from htmlmin.minify import html_minify


class CommandConsumer(AsyncJsonWebsocketConsumer):
    """Communicates with the browser to perform actions on-demand."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__logger = log.get_logger(__name__)

    # INITIAL CONNECTION
    async def connect(self):
        """When the browser attempts to connect to the server."""
        # Accept the connection
        await self.accept()

        # Attempt logging in the user
        try:
            # Log in the user to this session.
            await login(self.scope, self.scope["user"])
            # Save the session to the database
            await database_sync_to_async(self.scope["session"].save)()
        except:
            # User could not be logged in
            log.handler(
                "Websocket login failure on initial connection!",
                log.ERROR,
                self.__logger,
            )
            await self.__forbidden()

    # SENDING COMMANDS
    async def send_json(self, content, close=False):
        """Encode the given content as JSON and send it to the client."""
        # Minify HTML (if possible)
        if isinstance(content, dict) and content.__contains__("html"):
            content["html"] = html_minify(content["html"])

        # Send response
        await super().send(text_data=await self.encode_json(content), close=close)

    # RECEIVING COMMANDS
    async def receive_json(self, content, **kwargs):
        """When the browser attempts to send a message to the server."""
        log.handler(
            content,
            log.INFO,
            self.__logger,
        )
        # Reject users that aren't logged in
        if (
            isinstance(self.scope["user"], AnonymousUser)
            or not self.scope["user"].is_authenticated
        ):
            await self.__forbidden()
        else:
            if content["command_name"] == "server settings":
                await self.__server_settings(content)

            else:
                log.handler(
                    "Invalid websocket command.",
                    log.ERROR,
                    self.__logger,
                )

    # COMMAND RESPONSE: SERVER SETTINGS
    async def __server_settings(self, content):
        conreq_config = await database_sync_to_async(ConreqConfig.get_solo)()
        response = {
            "command_name": "server settings",
            "success": True,
            "error_message": "Failed to save settings. Check logs for details.",
        }

        # Validate user is admin before changing settings
        if self.scope["user"].is_staff:
            try:
                # Basic Configuration
                if content["parameters"]["setting_name"] == "Conreq Application Name":
                    conreq_config.conreq_app_name = content["parameters"]["value"]

                elif (
                    content["parameters"]["setting_name"]
                    == "Conreq Application URL/Web Domain"
                ):
                    conreq_config.conreq_app_url = content["parameters"]["value"]

                elif content["parameters"]["setting_name"] == "Conreq API Key":
                    conreq_config.conreq_api_key = secrets.token_hex(16)
                    await self.send_json(
                        {
                            "command_name": "new conreq api key",
                            "value": conreq_config.conreq_api_key,
                        }
                    )

                elif content["parameters"]["setting_name"] == "Conreq Language":
                    conreq_config.conreq_language = content["parameters"]["value"]

                elif content["parameters"]["setting_name"] == "Conreq Custom CSS":
                    conreq_config.conreq_custom_css = content["parameters"]["value"]

                elif content["parameters"]["setting_name"] == "Conreq Custom JS":
                    conreq_config.conreq_custom_js = content["parameters"]["value"]

                elif (
                    content["parameters"]["setting_name"]
                    == "Conreq Automatically Resolve Issues"
                ):
                    conreq_config.conreq_auto_resolve_issues = content["parameters"][
                        "value"
                    ]

                elif (
                    content["parameters"]["setting_name"]
                    == "Conreq Allow Guest Login/Requests"
                ):
                    conreq_config.conreq_guest_login = content["parameters"]["value"]

                elif (
                    content["parameters"]["setting_name"]
                    == "Conreq Simple/Minimal Poster Cards"
                ):
                    conreq_config.conreq_simple_posters = content["parameters"]["value"]

                elif content["parameters"]["setting_name"] == "Conreq Dark Theme":
                    conreq_config.conreq_dark_theme = content["parameters"]["value"]

                # Sonarr Settings
                elif content["parameters"]["setting_name"] == "Sonarr URL":
                    conreq_config.sonarr_url = content["parameters"]["value"]

                elif content["parameters"]["setting_name"] == "Sonarr API Key":
                    conreq_config.sonarr_api_key = content["parameters"]["value"]

                elif (
                    content["parameters"]["setting_name"]
                    == "Sonarr Anime Quality Profile"
                ):
                    conreq_config.sonarr_anime_quality_profile = content["parameters"][
                        "value"
                    ]

                elif (
                    content["parameters"]["setting_name"] == "Sonarr TV Quality Profile"
                ):
                    conreq_config.sonarr_tv_quality_profile = content["parameters"][
                        "value"
                    ]

                elif (
                    content["parameters"]["setting_name"] == "Sonarr Anime Folder Path"
                ):
                    conreq_config.sonarr_anime_folder = content["parameters"]["value"]

                elif content["parameters"]["setting_name"] == "Sonarr TV Folder Path":
                    conreq_config.sonarr_tv_folder = content["parameters"]["value"]

                elif content["parameters"]["setting_name"] == "Enable Sonarr":
                    conreq_config.sonarr_enabled = content["parameters"]["value"]

                elif content["parameters"]["setting_name"] == "Sonarr Season Folders":
                    conreq_config.sonarr_season_folders = content["parameters"]["value"]

                # Radarr Settings
                elif content["parameters"]["setting_name"] == "Radarr URL":
                    conreq_config.radarr_url = content["parameters"]["value"]

                elif content["parameters"]["setting_name"] == "Radarr API Key":
                    conreq_config.radarr_api_key = content["parameters"]["value"]

                elif (
                    content["parameters"]["setting_name"]
                    == "Radarr Anime Quality Profile"
                ):
                    conreq_config.radarr_anime_quality_profile = content["parameters"][
                        "value"
                    ]

                elif (
                    content["parameters"]["setting_name"]
                    == "Radarr Movies Quality Profile"
                ):
                    conreq_config.radarr_movies_quality_profile = content["parameters"][
                        "value"
                    ]

                elif (
                    content["parameters"]["setting_name"] == "Radarr Anime Folder Path"
                ):
                    conreq_config.radarr_anime_folder = content["parameters"]["value"]

                elif (
                    content["parameters"]["setting_name"] == "Radarr Movies Folder Path"
                ):
                    conreq_config.radarr_movies_folder = content["parameters"]["value"]

                elif content["parameters"]["setting_name"] == "Enable Radarr":
                    conreq_config.radarr_enabled = content["parameters"]["value"]

                # Unhandled setting failure
                else:
                    log.handler(
                        'Server setting "'
                        + content["parameters"]["setting_name"]
                        + '" is currently not handled!',
                        log.WARNING,
                        self.__logger,
                    )
                    response["success"] = False
                    response["error_message"] = "Unhandled server setting!"

                # Model fails validation schema
                try:
                    conreq_config.clean_fields()
                except ValidationError as error:
                    for field, message in dict(error).items():
                        response["success"] = False
                        response["error_message"] = field + ": " + message[0]
                        # Send a message to the user
                        await self.send_json(response)

                # Save the model if it passes all checks
                if response["success"]:
                    await database_sync_to_async(conreq_config.save)()

            except:
                response["success"] = False
                log.handler(
                    "Unknown error has occurred within server websocket!",
                    log.ERROR,
                    self.__logger,
                )

            # Send a message to the user
            await self.send_json(response)

        else:
            await self.__forbidden()

    # COMMAND RESPONSE: FORBIDDEN
    async def __forbidden(self):
        response = {"command_name": "forbidden"}
        await self.send_json(response)
