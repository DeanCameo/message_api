from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from .models import Message
from .serializers import MessageSerializer, UserSerializer



@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    login_view = ObtainAuthToken.as_view()
    response = login_view(request._request)
    token = Token.objects.get(key=response.data['token'])
    return Response({'token': token.key})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def write_message(request):
    if request.method == 'POST':
        sender_pk = request.user.pk
        data = request.data.copy()
        data['sender'] = sender_pk
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_messages(request, user):
    if request.method == 'GET':
        messages = Message.objects.filter(receiver=user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    return Response({"error": "Method not allowed"}, status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_messages(request, user):
    if request.method == 'GET':
        messages = Message.objects.filter(receiver=user, is_read=False)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    return Response({"error": "Method not allowed"}, status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_message(request, pk):
    if request.method == 'GET':
        message = get_object_or_404(Message, pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    return Response({"error": "Method not allowed"}, status=405)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_message(request, pk):
    if request.method == 'DELETE':
        message = get_object_or_404(Message, pk=pk)
        message.delete()
        return Response({'message': 'Message deleted successfully'}, status=204)
    return Response({"error": "Method not allowed"}, status=405)



