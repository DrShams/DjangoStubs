from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, PostSerializer, LoginSerializer
import random
import string

# Simple in-memory session storage
sessions = set()

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
            password = serializer.validated_data["password"]
            # Very simple logic: accept any username/password
            sessions.add(username)
            return Response({"message": f"{username} logged in"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            if username in sessions:
                sessions.remove(username)
                return Response({"message": f"{username} logged out"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "user not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
