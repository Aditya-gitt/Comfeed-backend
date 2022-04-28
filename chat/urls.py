from django.urls import path

from chat.views import getChat, postFeed , searchForChat, upvote, downvote
urlpatterns = [
    path('chat/post/', postFeed),
    path('chat/get/', getChat),
    # path('chat/search/', searchForChat)
    path('chat/upvote/', upvote),
    path('chat/downvote/', downvote)
]