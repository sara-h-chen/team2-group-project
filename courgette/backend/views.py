from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
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

# def createUser(request):
#     if request.method == 'POST':
#         serializer = UserCreationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# May not be required
def authenticate(request, username=None, password=None):
    try:
        user = User.objects.get(username)
        loginValid = check_password(password, user.password)
        if loginValid:
            serializer = UserSerializer(user)
            return JSONResponse(serializer.data)
    except User.DoesNotExist:
        user = User(username=username, password=password)
        user.save()
        serializer = UserSerializer(user)
        return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)


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


#########################################################
#                FOOD-RELATED QUERIES                   #
#########################################################


@login_required(login_url='backend/accounts/login/')
@csrf_exempt
def foodList(request, latitude, longitude):
    if request.method == 'GET':
        allFoods = Food.objects.filter(latitude__range=(latitude + 10), longitude__range=(longitude + 10))
        serializer = FoodSerializer(allFoods, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FoodSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


# Searches based on keyword, food_type, and location
def search(request, query):
    searchItems = Food.objects.get(Q(food_name__icontains=query) | Q(food_type__exact=query) |
                                   Q(location__icontains=query))
    serializer = FoodSerializer(searchItems, many=True)
    return JSONResponse(serializer.data)


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
