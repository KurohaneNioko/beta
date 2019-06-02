from django.urls import path

from . import consumer

websocket_urlpatterns = [  # 路由，指定 websocket 链接对应的 consumer
    path('ws/msg<int:uid>/', consumer.ChatConsumer),
]
