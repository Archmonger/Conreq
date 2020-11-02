import json

# from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.consumer import AsyncConsumer

# from channels.generic.websocket import WebsocketConsumer

# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model


class CommandConsumer(AsyncConsumer):
    """tmp"""

    async def websocket_connect(self, event):
        """tmp"""
        print("connected", event)
        await self.send({"type": "websocket.accept"})

    async def websocket_disconnect(self, event):
        """tmp"""
        print("disconnected", event)

    async def websocket_receive(self, event):
        """tmp"""
        print("received", event)
