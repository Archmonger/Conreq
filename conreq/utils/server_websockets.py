"""Anything used to construct a websocket endpoint"""
from channels.auth import AnonymousUser, login
from channels.db import database_sync_to_async as convert_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from conreq.utils import log

__logger = log.get_logger(__name__)


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
            await convert_to_async(self.scope["session"].save)()
        except:
            # User could not be logged in
            log.handler(
                "Websocket login failure on initial connection!",
                log.ERROR,
                __logger,
            )
            await self.__forbidden()

    # RECEIVING COMMANDS
    async def receive_json(self, content, **kwargs):
        """When the browser attempts to send a message to the server."""
        log.handler(
            content,
            log.INFO,
            __logger,
        )
        # Reject users that aren't logged in
        if (
            isinstance(self.scope["user"], AnonymousUser)
            or not self.scope["user"].is_authenticated
        ):
            await self.__forbidden()

    # COMMAND RESPONSE: FORBIDDEN
    async def __forbidden(self):
        response = {"command_name": "forbidden"}
        await self.send_json(response)
