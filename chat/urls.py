from django.urls import path

from chat.views import getChat, postFeed

urlpatterns = [
    path('chat/post/', postFeed),
    path('chat/get/', getChat),
]