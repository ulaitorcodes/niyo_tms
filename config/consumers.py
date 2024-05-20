import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RealTimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass  # No action required on disconnect

    async def receive(self, text_data):
        # Handle received data
        pass

    async def send_realtime_data(self, event):
        # Send real-time data to WebSocket
        await self.send(text_data=json.dumps(event['data']))
