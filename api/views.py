from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, PostSerializer, LoginSerializer
import random
import string
import uuid

# Simple in-memory session storage
sessions = {}

class UserView(APIView):
    def get(self, request, id):
        # generate random text for name
        name = ''.join(random.choices(string.ascii_letters, k=20))
        data = {"id": id, "name": name}
        serializer = UserSerializer(data)
        return Response(serializer.data)

class PostView(APIView):
    def post(self, request, id):
        # get input JSON
        input_data = request.data
        input_data["id"] = id
        serializer = PostSerializer(data=input_data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
           # генерируем уникальный session_id
            session_id = str(uuid.uuid4())
            sessions[session_id] = username
            # Very simple logic: accept any username/password
            #sessions.add(username)
            return Response({
                "message": f"{username} logged in",
                "session_id": session_id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        # Получаем session_id из заголовка Authorization
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            session_id = auth_header.split(" ")[1]
            if session_id in sessions:
                username = sessions.pop(session_id)  # удаляем сессию и получаем username
                return Response({"message": f"{username} logged out"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "invalid session"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "missing or invalid Authorization header"}, status=status.HTTP_400_BAD_REQUEST)

