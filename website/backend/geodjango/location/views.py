from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from location.models import Location
from location.serializers import LocationSerializer

# Create your views here.

class JSONResponse(HttpResponse):
    """
    A HttpResponse that renders its contents into JSON
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def location_list(request):
    """
    List all locations, or create a new location
    """
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def location_detail(request, pk):
    """
    Retrieve, update or delete a location
    """
    try:
        location = Location.objects.get(pk=pk)
    except Location.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LocationSerializer(location)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LocationSerializer(location, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        location.delete()
        return HttpResponse(status=204)

