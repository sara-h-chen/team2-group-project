from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from serializers import FoodSerializer, MessageSerializer, UserSerializer
from models import User, Food, Message

###################################################################
#                     VIEWS IN REGULAR DJANGO                     #
###################################################################


def index(request):
    # RETURN INDEX HTML PAGE ON COMMUNITY.DUR.AC.UK
    return HttpResponse("Placeholder simple Index page.")


# RETURNS FOOD LISTING
def food_listing(request):
    latest_food_requests = Food.objects.order_by('Date listed')
    output = ', '.join([food.food_name for food in latest_food_requests])
    return HttpResponse(output)


def search(request):
    output = 'search'
    return HttpResponse(output)


def notification(request):
    output = 'notifcation'
    return HttpResponse(output)


# GETS THE USERNAME FROM THE URL AS A PARAM
def user_page(request, username):
    # GET PARTICULAR USER FROM DB BASED ON PARAM
    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return JSONResponse(serializer.data)
    except:
        return HttpResponse(404)


#########################################################################
#                VIEWS USING CLASS-BASED DJANGO REST                    #
#########################################################################


class JSONResponse(HttpResponse):
    """
    A HttpResponse that renders content into JSON
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def food_list(request, location):
    if request.method == 'GET':
        allFoods = Food.objects.filter(location=location)
        serializer = FoodSerializer(allFoods, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FoodSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


def getMessages(request, username):
    try:
        messageList = Message.objects.filter(sender=username)
        serializer = MessageSerializer(messageList, many=True)
        return JSONResponse(serializer.data)
    except Message.DoesNotExist:
        return JSONResponse(status=status.HTTP_404_NOT_FOUND)