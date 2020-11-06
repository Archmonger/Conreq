from channels.generic.websocket import AsyncJsonWebsocketConsumer

from conreq import content_manager
from conreq.apps.more_info.views import series_modal

# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# from pprint import pprint


class CommandConsumer(AsyncJsonWebsocketConsumer):
    """Communicates with the browser to perform actions on-demand."""

    # BASIC WEBSOCKET FUNCTIONALITY

    async def connect(self):
        """When the browser attempts to connect to the server."""
        print("connected")
        await self.accept()
        # pprint(self.scope)

    # RECIEVABLE COMMANDS

    async def receive_json(self, content, **kwargs):
        """When the browser attempts to send a message to the server."""
        print("received", content)
        if isinstance(content, dict) and content.__contains__("command_name"):
            # Request command
            if content["command_name"] == "request":
                await self.__request_command(content)
            if content["command_name"] == "series selection modal":
                await self.__series_selection_modal_command(content)

        else:
            print("invalid websocket structure")

    # SENDABLE COMMANDS

    async def __request_command(self, content):
        if (
            isinstance(content["parameters"], dict)
            and content.__contains__("parameters")
            and content["parameters"].__contains__("content_type")
        ):
            # TV show was requested
            if (
                content["parameters"].__contains__("tvdb_id")
                and content["parameters"]["tvdb_id"] is not None
            ) or (
                content["parameters"].__contains__("tmdb_id")
                and content["parameters"]["content_type"] == "tv"
            ):
                print("requested tv")

            # Movie was requested
            elif (
                content["parameters"].__contains__("tmdb_id")
                and content["parameters"]["content_type"] == "movie"
            ):
                # TODO: Obtain radarr root and quality profile ID from database
                radarr_root = content_manager.radarr_root_dirs()[0]["path"]
                preexisting_movie = content_manager.get(
                    tmdb_id=content["parameters"]["tmdb_id"]
                )
                if preexisting_movie is None:
                    new_movie = content_manager.add(
                        tmdb_id=content["parameters"]["tmdb_id"],
                        quality_profile_id=1,
                        root_dir=radarr_root,
                    )
                    if new_movie.__contains__("id"):
                        content_manager.request(radarr_id=new_movie["id"])
                    else:
                        print("new movie did not contain id")
                else:
                    content_manager.request(radarr_id=preexisting_movie["id"])
                print("requested movie")
            print("Request checks have passed")
        else:
            print("Request is missing parameters!")

    async def __series_selection_modal_command(self, content):
        # command_name
        # response
        response = {"command_name": "series selection modal", "html": None}
        if isinstance(content["parameters"], dict) and content.__contains__(
            "parameters"
        ):
            # TV show was requested
            if (
                content["parameters"].__contains__("tvdb_id")
                and content["parameters"]["tvdb_id"] is not None
            ) or (
                content["parameters"].__contains__("tmdb_id")
                and content["parameters"]["content_type"] == "tv"
            ):
                response["html"] = series_modal(1)
                await self.send_json(response)
                print("Series selection modal generated")
            else:
                print("Series selection modal missing an ID")

        else:
            print("Series selection modal  is missing parameters!")
