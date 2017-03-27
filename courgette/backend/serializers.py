from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from models import Food, Message
from django.contrib.auth.models import User


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('food_name', 'quantity', 'date_listed', 'food_type', 'allergens',
                  'status', 'latitude', 'longitude', 'user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


# TODO: Fix the relations
class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format=None, input_formats=None)
    sender = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ('sender', 'receiver', 'msg_content', 'created_at', 'read')


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')