from tokenize import String
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from chat.models import Chat
from chat.serializers import GetChatSerializer, PostFeedSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


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
    data["upvotes"] = {}
    data["downvotes"] = {}
    return data

@api_view(['post'])
@permission_classes([AllowAny,])
def getChat(request):
    context = {'id': request.data['user_id']}
    serializer = GetChatSerializer(get_chat(request), context=context, many=True)
    return JsonResponse({
        "chats": serializer.data,
        "has_more": has_more(int(request.GET.get('offset'))) 
    }, status=status.HTTP_200_OK)

def get_chat(request):
    limit = int(request.GET.get('limit'))
    offset = int(request.GET.get('offset'))
    chats = list(Chat.objects.all().order_by('-date').order_by('-time')[offset: offset + limit])
    return chats

def has_more(offset):
    if int(offset) > Chat.objects.all().count():
        return False
    return True

@api_view(['post'])
@permission_classes([IsAuthenticated,])
def searchForChat(request):
    context = {'id': request.data['user_id']}
    serializer = GetChatSerializer(searchChats(request), context=context, many=True)
    return JsonResponse({
        "chats": serializer.data,
        "has_more": has_more(int(request.GET.get('offset'))) 
    }, status=status.HTTP_200_OK)

#json_array_contains('tags'," + request.GET.get('tag') + ")"
def searchChats(request):
    tag = request.data.get('tags')
    limit = int(request.GET.get('limit'))
    offset = int(request.GET.get('offset'))
    query = "SELECT * from chat_chat where tags like " + "'%" + str(tag) + "%' order by date, time"
    chats = list(Chat.objects.raw(query)[offset: offset + limit])
    return chats

@api_view(['post'])
@permission_classes([IsAuthenticated,])
def upvote(request):
    upvoter = User.objects.get(id=request.data['author_id'])
    if Chat.objects.get(chat_id=request.data['chat_id']).upvotes.filter(id=request.data['author_id']).exists():
        Chat.objects.get(chat_id=request.data['chat_id']).upvotes.remove(upvoter)
    else :
        if Chat.objects.get(chat_id=request.data['chat_id']).downvotes.filter(id=request.data['author_id']).exists():
            Chat.objects.get(chat_id=request.data['chat_id']).downvotes.remove(upvoter)
            Chat.objects.get(chat_id=request.data['chat_id']).upvotes.add(upvoter)
        else :
            Chat.objects.get(chat_id=request.data['chat_id']).upvotes.add(upvoter)
    return Response(status.HTTP_202_ACCEPTED)

@api_view(['post'])
@permission_classes([IsAuthenticated,])
def downvote(request):
    upvoter = User.objects.get(id=request.data['author_id'])
    if Chat.objects.get(chat_id=request.data['chat_id']).downvotes.filter(id=request.data['author_id']).exists():
        Chat.objects.get(chat_id=request.data['chat_id']).downvotes.remove(upvoter)
    else :
        if Chat.objects.get(chat_id=request.data['chat_id']).upvotes.filter(id=request.data['author_id']).exists():
            Chat.objects.get(chat_id=request.data['chat_id']).upvotes.remove(upvoter)
            Chat.objects.get(chat_id=request.data['chat_id']).downvotes.add(upvoter)
        else :
            Chat.objects.get(chat_id=request.data['chat_id']).downvotes.add(upvoter)
    return Response(status.HTTP_202_ACCEPTED)

