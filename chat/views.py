from turtle import pos
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from chat.models import Chat
from chat.serializers import GetChatSerializer, PostFeedSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['post'])
@permission_classes([IsAuthenticated,])
def postFeed(request):
    postSerializer = PostFeedSerializer(data=get_chat_model(request.data))
    if postSerializer.is_valid():
        postSerializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return JsonResponse(postSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_chat_model(data):
    #model = Chat(data)
    # model.downvotes.clear()
    # model.upvotes.clear()
    data["upvotes"] = {}
    data["downvotes"] = {}
    return data

@api_view(['get'])
@permission_classes([AllowAny,])
def getChat(request):
    serializer = GetChatSerializer(get_chat(request), many=True)
    return JsonResponse({
        "chats": serializer.data,
        "has_more": has_more(int(request.GET.get('offset'))) 
    }, status=status.HTTP_200_OK)

def get_chat(request):
    limit = int(request.GET.get('limit'))
    offset = int(request.GET.get('offset'))
    chats = list(Chat.objects.all()[offset: offset + limit])
    return chats

def has_more(offset):
    if int(offset) > Chat.objects.all().count():
        return False
    return True