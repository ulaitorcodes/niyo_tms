# routing.py

from django.urls import path
from .consumers import RealTimeConsumer

websocket_urlpatterns = [
    path('ws/realtime/', RealTimeConsumer.as_asgi()),
]
