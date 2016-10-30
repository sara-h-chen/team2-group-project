from rest_framework import serializers
from location.models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('locationName', 'xcoordinate', 'ycoordinate')

    #id = serializers.IntegerField(read_only=True)
    #locationName = serializers.CharField(required=False, allow_blank=True, max_length=200)

    #def create(self, validated_data):
    #    """
    #    Create and return a new 'Location' instance, given the validated data
    #    """
    #    return Location.objects.create(**validated_data)

    #def update(self, instance, validated_data):
    #    """
    #    Update and return an existing 'Location' instance, given the validated data
    #    """
    #    instance.locationName = validated_data.get('locationName', instance.locationName)
    #    instance.save()
    #    return instance
