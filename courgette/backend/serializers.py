from rest_framework import serializers
from models import Food, Message
from django.contrib.auth.models import User


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('food_name', 'quantity', 'date_listed', 'food_type', 'allergens', 'status', 'location', 'user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('sender', 'receiver', 'msg_content', 'created_at', 'read')


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')