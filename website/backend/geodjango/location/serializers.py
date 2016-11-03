from rest_framework import serializers
from location.models import Location, Test
from django.contrib.auth.models import User

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('locationName', 'xcoordinate', 'ycoordinate', 'owner')
        owner = serializers.ReadOnlyField(source='owner.username')

class UserSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(many=True, queryset=Location.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'location')

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('ratings', 'name', 'location')
