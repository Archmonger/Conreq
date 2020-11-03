from channels.generic.websocket import AsyncJsonWebsocketConsumer

# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# from pprint import pprint


class CommandConsumer(AsyncJsonWebsocketConsumer):
    """Communicates with the browser to perform actions on-demand."""

    async def connect(self):
        """When the browser attempts to connect to the server."""
        print("connected")
        await self.accept()
        await self.send_json({"test": "testy"})
        # pprint(self.scope)

    async def receive_json(self, content, **kwargs):
        """When the browser attempts to send a message to the server."""
        print("received", content)
