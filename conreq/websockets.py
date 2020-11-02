import json

from channels.consumer import AsyncConsumer

# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model


class CommandConsumer(AsyncConsumer):
    """tmp"""

    async def websocket_connect(self, event):
        """tmp"""
        print("connected", event)
        await self.send({"type": "websocket.accept"})
        tmp_json = json.dumps({"test": "testy"})
        await self.send({"type": "websocket.send", "text": tmp_json})

    async def websocket_disconnect(self, event):
        """tmp"""
        print("disconnected", event)

    async def websocket_receive(self, event):
        """tmp"""
        print("received", event)
