"""Conreq's main websockets."""
import logging

from channels.auth import login
from channels.db import database_sync_to_async as convert_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

_logger = logging.getLogger(__name__)


class BaseWebsocket(AsyncJsonWebsocketConsumer):
    """
    Conreq's base websocket. Performs basic tasks such as letting client
    browsers know if a page refresh is needed.
    """

    async def connect(self):
        """Event that occurs when the browser attempts to connect to the server."""
        # Accept any connection
        await self.accept()

        # Attempt logging in the user
        try:
            if self.scope["user"].is_authenticated:
                # Log in the user to this session
                await login(self.scope, self.scope["user"])
                # Save the session to the database
                await convert_to_async(self.scope["session"].save)()
            else:
                # Signal that the user shouldn't be here
                await self.__forbidden()

        # User could not be logged in
        except Exception:
            _logger.exception("Websocket login failure on initial connection!")
            await self.__forbidden()

    async def receive_json(self, content, **kwargs):
        """Event that occurs when the browser sent a message to the server."""
        _logger.info("Message received: %s", content)

        # Reject users that aren't logged in
        if not self.scope["user"].is_authenticated:
            await self.__forbidden()

    async def __forbidden(self):
        """Notify an unauthenticated user that they shouldn't be here."""
        await self.send_json({"command_name": "forbidden"})