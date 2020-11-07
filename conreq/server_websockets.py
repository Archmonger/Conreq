from channels.generic.websocket import AsyncJsonWebsocketConsumer

from conreq import content_manager
from conreq.apps.more_info.views import series_modal

# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# from pprint import pprint


class CommandConsumer(AsyncJsonWebsocketConsumer):
    """Communicates with the browser to perform actions on-demand."""

    # INITIAL CONNECTION
    async def connect(self):
        """When the browser attempts to connect to the server."""
        print("connected")
        await self.accept()
        # pprint(self.scope)

    # RECIEVABLE COMMANDS
    async def receive_json(self, content, **kwargs):
        """When the browser attempts to send a message to the server."""
        print("received", content)

        if content["command_name"] == "request":
            await self.__request_content(content)

        elif content["command_name"] == "generate modal":
            await self.__generate_modal(content)

        else:
            print("invalid websocket structure")

    # COMMAND RESPONSE: REQUEST CONTENT
    async def __request_content(self, content):
        # TV show was requested
        if content["parameters"]["content_type"] == "tv":
            print("requested tv")

        # Movie was requested
        elif content["parameters"]["content_type"] == "movie":
            # TODO: Obtain radarr root and quality profile ID from database
            radarr_root = content_manager.radarr_root_dirs()[0]["path"]

            # Check if the movie is already within Radarr's collection
            preexisting_movie = content_manager.get(
                tmdb_id=content["parameters"]["tmdb_id"]
            )

            # If it doesn't already exists, add then request it
            if preexisting_movie is None:
                new_movie = content_manager.add(
                    tmdb_id=content["parameters"]["tmdb_id"],
                    quality_profile_id=1,
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
        response = {"command_name": "generate modal", "html": None}
        if (
            content["parameters"]["tvdb_id"] is not None
            or content["parameters"]["tmdb_id"] is not None
        ):
            response["html"] = series_modal(1)
            await self.send_json(response)
        else:
            print("Generate modal missing an ID!")
