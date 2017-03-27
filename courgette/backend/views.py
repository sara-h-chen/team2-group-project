from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from serializers import FoodSerializer, MessageSerializer, UserSerializer, UserCreationSerializer
from models import Food, Message, UserForm


#########################################################
#                USER-RELATED QUERIES                   #
#########################################################


def index(request):
    # TODO: Return index page/remove this
    return HttpResponse("Placeholder simple Index page.")


# Create user through POST request
def createUser(request):
    if request.method == "POST":
        form = UserForm()
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return HttpResponse('../website/index.html')
    else:
        form = UserForm()

    return render(request, 'backend/adduser.html', {'form': form})


# UNUSED: RETURNS FOOD LISTING (for reference only!)
# def food_listing(request):
#     latest_food_requests = Food.objects.order_by('Date listed')
#     output = ', '.join([food.food_name for food in latest_food_requests])
#     return HttpResponse(output)


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

@login_required(login_url='/login/')
@csrf_exempt
def foodList(request, latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)
    if request.method == 'GET':
        allFoods = Food.objects.filter(latitude__range=(latitude + 10, longitude + 10))
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
        user = User.objects.filter(username=username)
        uID = user[0].id
        messageList = Message.objects.filter(Q(receiver_id=0) | Q(sender_id=0))
        serializer = MessageSerializer(messageList, many=True)
        return JSONResponse(serializer.data)
    except Message.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


def getContacts(request, username):
    try:
        user = User.objects.filter(username=username)
        uID = user[0].id
        messageList = Message.objects.filter(Q(receiver_id=0) | Q(sender_id=0))
        contacts = []
        for x in messageList:
            if x.receiver_id == uID:
                if x.sender_id not in contacts:
                    contacts.append(x.sender_id)
            elif x.sender_id == uID:
                if x.receiver_id not in contacts:
                    contacts.append(x.receiver_id)
        print contacts
        serializer = MessageSerializer(messageList, many=True)
        return JSONResponse(serializer.data)
    except Message.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def addMessage(request, username):
    try:
        if request.method == "POST":
            data =request.POST
            sender_id=data['sender_id']
            receiver_id = data['receiver_id']
            msg_content=data['msg_content']
            # user=User.objects.filter(username=sender_username)
            # sender_id=user[0].id
            # user=User.objects.filter(username=receiver_username)
            # receiver_id=user[0].id
            message= Message(sender_id=sender_id,receiver_id=receiver_id,msg_content=msg_content)
            return JSONResponse("{'done:done'}")
        # message.save()
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
