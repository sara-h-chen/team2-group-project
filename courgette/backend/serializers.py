from rest_framework import serializers
from .models import User, Food

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        # fields = ('food_name', 'quantity', 'date_listed', 'food_type', 'allergens', 'status')

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, allow_blank=False, max_length=200)