from django.urls import path
from .consumer import NewsConsumer

websocket_urlpatterns = [
    path('ws/news_streaming/', NewsConsumer),
    path('wss/news_streaming/', NewsConsumer),
]
