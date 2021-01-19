from channels.auth import AnonymousUser, login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.management.utils import get_random_secret_key
from htmlmin.minify import html_minify

from conreq.apps.helpers import obtain_sonarr_parameters
from conreq.apps.more_info.views import series_modal
from conreq.apps.server_settings.models import ConreqConfig
from conreq.core.content_discovery import ContentDiscovery
from conreq.core.content_manager import ContentManager


class CommandConsumer(AsyncJsonWebsocketConsumer):
    """Communicates with the browser to perform actions on-demand."""

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
        except Exception as exception:
            # User could not be logged in
            print(str(exception))
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
        print(content)
        # Reject users that aren't logged in
        if (
            isinstance(self.scope["user"], AnonymousUser)
            or not self.scope["user"].is_authenticated
        ):
            await self.__forbidden()
        else:
            # Verify login status.
            await login(self.scope, self.scope["user"])

            # Process the command
            if content["command_name"] == "request":
                await self.__request_content(content)

            elif content["command_name"] == "generate modal":
                await self.__generate_modal(content)

            elif content["command_name"] == "server settings":
                await self.__server_settings(content)

            else:
                print("Invalid websocket command")

    # COMMAND RESPONSE: REQUEST CONTENT
    async def __request_content(self, content):
        content_manager = await database_sync_to_async(ContentManager)()
        content_discovery = ContentDiscovery()

        # TV show was requested
        if content["parameters"]["content_type"] == "tv":
            # Obtain the TVDB ID if needed
            tvdb_id = content["parameters"]["tvdb_id"]
            tmdb_id = content["parameters"]["tmdb_id"]
            if tvdb_id is None and tmdb_id is not None:
                tvdb_id = content_discovery.get_external_ids(tmdb_id, "tv")["tvdb_id"]

            # Request the show by the TVDB ID
            if tvdb_id is not None:
                # Check if the show is already within Sonarr's collection
                preexisting_show = content_manager.get(tvdb_id=tvdb_id)

                # If it doesn't already exists, add then request it
                if preexisting_show is None:
                    sonarr_params = await database_sync_to_async(
                        obtain_sonarr_parameters
                    )(content_discovery, content_manager, tmdb_id, tvdb_id)
                    new_show = content_manager.add(
                        tvdb_id=tvdb_id,
                        quality_profile_id=sonarr_params["sonarr_profile_id"],
                        root_dir=sonarr_params["sonarr_root"],
                        series_type=sonarr_params["series_type"],
                        season_folders=sonarr_params["season_folders"],
                    )
                    if new_show.__contains__("id"):
                        content_manager.request(
                            sonarr_id=new_show["id"],
                            seasons=content["parameters"]["seasons"],
                            episode_ids=content["parameters"]["episode_ids"],
                        )
                        print("requested tv")
                    else:
                        print(
                            "Show was added to Sonarr, but Sonarr did not return an ID!"
                        )
                else:
                    content_manager.request(
                        sonarr_id=preexisting_show["id"],
                        seasons=content["parameters"]["seasons"],
                        episode_ids=content["parameters"]["episode_ids"],
                    )

        # Movie was requested
        elif content["parameters"]["content_type"] == "movie":
            radarr_params = await database_sync_to_async(obtain_radarr_parameters)(
                content_discovery, content_manager, content["parameters"]["tmdb_id"]
            )

            # Check if the movie is already within Radarr's collection
            preexisting_movie = content_manager.get(
                tmdb_id=content["parameters"]["tmdb_id"]
            )

            # If it doesn't already exists, add then request it
            if preexisting_movie is None:
                new_movie = content_manager.add(
                    tmdb_id=content["parameters"]["tmdb_id"],
                    quality_profile_id=radarr_profile_id,
                    root_dir=radarr_root,
                )
                if new_movie.__contains__("id"):
                    content_manager.request(radarr_id=new_movie["id"])
                else:
                    print("Movie was added to Radarr, but Radarr did not return an ID!")

            # If it already existed, just request it
            else:
                content_manager.request(radarr_id=preexisting_movie["id"])

    # COMMAND RESPONSE: GENERATE MODAL
    async def __generate_modal(self, content):
        response = {
            "command_name": "render page element",
            "selector": "#modal-content",
            "html": None,
        }

        # Check if an ID is present
        if (
            content["parameters"]["tvdb_id"] is not None
            or content["parameters"]["tmdb_id"] is not None
        ):
            # Episode modal
            if content["parameters"]["modal_type"] == "episode selector":
                response["html"] = await database_sync_to_async(series_modal)(
                    tmdb_id=content["parameters"]["tmdb_id"],
                    tvdb_id=content["parameters"]["tvdb_id"],
                )
                await self.send_json(response)

            # Content info modal
            elif content["parameters"]["modal_type"] == "content info":
                pass

            else:
                print("Invalid modal type!")
        else:
            print("Generate modal missing an ID!")

    # COMMAND RESPONSE: SERVER SETTINGS
    async def __server_settings(self, content):
        conreq_config = await database_sync_to_async(ConreqConfig.get_solo)()
        response = {"command_name": "server settings", "success": True}

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
                    conreq_config.conreq_api_key = get_random_secret_key()

                elif content["parameters"]["setting_name"] == "Conreq Language":
                    conreq_config.conreq_language = content["parameters"]["value"]

                elif content["parameters"]["setting_name"] == "Conreq Logo Image":
                    pass
                    # conreq_config.conreq_app_logo = content["parameters"]["value"]

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

                # Failure
                else:
                    print(
                        'Server setting "'
                        + content["parameters"]["setting_name"]
                        + '" is currently not handled!'
                    )
                    response["success"] = False

                if response["success"]:
                    await database_sync_to_async(conreq_config.save)()

            except:
                response["success"] = False

            # Send a message to the user
            await self.send_json(response)

        else:
            await self.__forbidden()

    # COMMAND RESPONSE: FORBIDDEN
    async def __forbidden(self):
        response = {"command_name": "forbidden"}
        await self.send_json(response)
