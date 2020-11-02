from channels.generic.websocket import AsyncJsonWebsocketConsumer

# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# from pprint import pprint


class CommandConsumer(AsyncJsonWebsocketConsumer):
    """tmp"""

    async def connect(self):
        """When the browser attempts to """
        print("connected")
        await self.accept()
        await self.send_json({"test": "testy"})
        # pprint(self.scope)

    async def receive_json(self, content, **kwargs):
        """When the browser attempts to communicate with the server."""
        print("received", content)
