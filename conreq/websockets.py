import json

from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# from pprint import pprint


class CommandConsumer(AsyncConsumer):
    """tmp"""

    async def websocket_connect(self, event):
        """When the browser attempts to """
        print("connected", event)
        await self.send({"type": "websocket.accept"})
        tmp_json = json.dumps({"test": "testy"})
        await self.send({"type": "websocket.send", "text": tmp_json})
        # pprint(self.scope)

    async def websocket_disconnect(self, event):
        """When the websocket connection closes."""
        print("disconnected", event)
        raise StopConsumer

    async def websocket_receive(self, event):
        """When the browser attempts to communicate with the server."""
        print("received", event)
