from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class PostSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
    userId = serializers.IntegerField()
    id = serializers.IntegerField(required=False)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

