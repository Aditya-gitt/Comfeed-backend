from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from folks.serializers import UserRegistrationSerializer
from rest_framework.response import Response

# Create your views here.


@api_view(['post'])
@permission_classes([AllowAny,])
def userRegistration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save()
        if new_user:
            return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
