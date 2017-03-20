from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.db.models import Q

from django.contrib.auth.models import User
from serializers import FoodSerializer, MessageSerializer, UserSerializer, UserCreationSerializer
from models import Food, Message


#########################################################
#                USER-RELATED QUERIES                   #
#########################################################


def index(request):
    # TODO: Return index page/remove this
    return HttpResponse("Placeholder simple Index page.")


## UNUSED: RETURNS FOOD LISTING (for reference only!)
# def food_listing(request):
#     latest_food_requests = Food.objects.order_by('Date listed')
#     output = ', '.join([food.food_name for food in latest_food_requests])
#     return HttpResponse(output)


# TODO: Implement a Search functionality?
def search(request):
    output = 'search'
    return HttpResponse(output)


# TODO: Return all users instead?
# Gets the username from the URL as a param
def findUser(request, username):
    # Get particular user from db based on param
    # Returns username and email
    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return JSONResponse(serializer.data)
    except:
        return HttpResponse('User not found')


def createUser(request):
    if request.method == 'POST':
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#########################################################
#                FOOD-RELATED QUERIES                   #
#########################################################


@csrf_exempt
def foodList(request, location):
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


#########################################################
#               MESSAGE-RELATED QUERIES                 #
#########################################################


# Returns number of unread messages
def unreadMessages(request, username):
    try:
        unreadMessages = Message.objects.filter(receiver=username, read=False).count()
        serialized = JSONRenderer().render(unreadMessages)
        return JSONResponse(serialized)
    except:
        return HttpResponse('User not found')


# Gets all the messages for current user and returns it
def getMessages(request, username):
    try:
        messageList = Message.objects.filter(Q(receiver__username=username) | Q(sender__username=username)) #TODO Check whether works with data in db
        serializer = MessageSerializer(messageList, many=True)
        return JSONResponse(serializer.data)
    except Message.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


##########################################################
#               DJANGO REST UTILITIES                    #
##########################################################


class JSONResponse(HttpResponse):
    """
    A HttpResponse that renders content into JSON
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
