from channels.auth import AnonymousUser, login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from htmlmin.minify import html_minify

from conreq import content_discovery, content_manager
from conreq.apps.more_info.views import series_modal


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
        print("received", content)
        # Reject users that aren't logged in
        if isinstance(self.scope["user"], AnonymousUser):
            await self.__forbidden()
        else:
            # Verify login status.
            await login(self.scope, self.scope["user"])

            # Process the command
            if content["command_name"] == "request":
                await self.__request_content(content)

            elif content["command_name"] == "generate modal":
                await self.__generate_modal(content)

            else:
                print("Invalid websocket command")

    # COMMAND RESPONSE: REQUEST CONTENT
    async def __request_content(self, content):
        # TV show was requested
        if content["parameters"]["content_type"] == "tv":
            # TODO: Obtain Sonarr root and quality profile ID from database
            sonarr_root = content_manager.sonarr_root_dirs()[0]["path"]
            sonarr_profile_id = content_manager.sonarr_quality_profiles()[0]["id"]

            # Obtain the TVDB ID if needed
            tvdb_id = content["parameters"]["tvdb_id"]
            tmdb_id = content["parameters"]["tmdb_id"]
            if tvdb_id is None and tmdb_id is not None:
                tvdb_id = content_discovery.get_external_ids(tmdb_id, "tv")["tvdb_id"]

            # print("tvdb ID ", tvdb_id)
            # Request the show by the TVDB ID
            if tvdb_id is not None:
                # Check if the show is already within Sonarr's collection
                preexisting_show = content_manager.get(tvdb_id=tvdb_id)

                # If it doesn't already exists, add then request it
                if preexisting_show is None:
                    new_show = content_manager.add(
                        tvdb_id=tvdb_id,
                        quality_profile_id=sonarr_profile_id,
                        root_dir=sonarr_root,
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
            # TODO: Obtain radarr root and quality profile ID from database
            radarr_root = content_manager.radarr_root_dirs()[0]["path"]
            radarr_profile_id = content_manager.radarr_quality_profiles()[0]["id"]

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
                response["html"] = series_modal(
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

    # COMMAND RESPONSE: FORBIDDEN
    async def __forbidden(self):
        response = {"command_name": "forbidden"}
        await self.send_json(response)
