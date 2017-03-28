from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework import status, permissions

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from serializers import FoodSerializer, MessageSerializer, UserSerializer, UserCreationSerializer
from models import Food, Message, UserForm

##########################################################
#                      HEADER CONTROL                    #
##########################################################


def _acao_response(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'


#########################################################
#                USER-RELATED QUERIES                   #
#########################################################


def index(request):
    # TODO: Return index page/remove this
    return HttpResponse("Placeholder simple Index page.")


@csrf_exempt
# Create user through POST request
def createUser(request):
    # if request.method == 'POST':
    form = UserForm(request.POST or None)
    if form.is_valid():
        new_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name']
        )
        login(request, new_user)
        response = HttpResponseRedirect('/')
        _acao_response(response)
        return response

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
        response = JSONResponse(serializer.data)
        _acao_response(response)
        return response
    except User.DoesNotExist:
        return HttpResponse('User not found')

def indentify(request, user_id):
    try:
        print user_id
        user=User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        response = JSONResponse(serializer.data)
        response['Access-Control-Allow-Origin']='*'
        return response
    except:
        return HttpResponse('User not found')


#########################################################
#                FOOD-RELATED QUERIES                   #
#########################################################

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def foodList(request, latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)
    if request.method == 'GET':
        allFoods = Food.objects.filter(Q(latitude__range=(latitude - 10, latitude + 10)),
                                       Q(longitude__range=(longitude - 10, longitude + 10)))
        serializer = FoodSerializer(allFoods, many=True)
        response = JSONResponse(serializer.data)
        _acao_response(response)
        return response

    elif request.method == 'POST':
        username = request.user.username
        currentUser = User.objects.get(username=username)
        data = JSONParser().parse(request)
        serializer = FoodSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=currentUser)
            response = JSONResponse(serializer.data, status=201)
            _acao_response(response)
            return response
        response = JSONResponse(serializer.errors, status=400)
        _acao_response(response)
        return response


# Searches based on keyword, food_type, and location
def search(request, query):
    searchItems = Food.objects.get(Q(food_name__icontains=query) | Q(food_type__exact=query) |
                                   Q(location__icontains=query))
    serializer = FoodSerializer(searchItems, many=True)
    response = JSONResponse(serializer.data)
    _acao_response(response)
    return response


# def update(request, )


#########################################################
#               MESSAGE-RELATED QUERIES                 #
#########################################################


# Returns number of unread messages
def unreadMessages(request, username):
    try:
        unreadMessages = Message.objects.filter(receiver=username, read=False).count()
        serialized = JSONRenderer().render(unreadMessages)
        response = JSONResponse(serialized)
        _acao_response(response)
        return response
    except:
        return HttpResponse('User not found')


# Gets all the messages for current user and returns it
def getMessages(request, username):
    try:
        user = User.objects.filter(username=username)
        uID = user[0].id
        messageList = Message.objects.filter(Q(receiver_id=0) | Q(sender_id=0))
        serializer = MessageSerializer(messageList, many=True)
        response = JSONResponse(serializer.data)
        _acao_response(response)
        return response
    except Message.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


def getContacts(request, username):
    try:
        user=User.objects.filter(username=username)
        uID=user[0].id
        messageList = Message.objects.filter(Q(receiver_id=uID) | Q(sender_id=uID))
        contacts={}
        contactList=[]
        counter=0
        for x in messageList:
            if x.receiver_id==uID:
                if not x.sender_id in contactList:
                    contactList.append(x.sender_id)
                    contacts[counter] = (x.sender_id)
                    counter=counter+1
            elif x.sender_id==uID:
                if not x.receiver_id in contactList:
                    contactList.append(x.receiver_id)
                    contacts[counter] = (x.receiver_id)
                    counter=counter+1
        response = JSONResponse(contacts)
        response['Access-Control-Allow-Origin']='*'
        return response
    except Message.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def addMessage(request, username):
    try:
        if request.method == "POST":#TODO make robust i.e. deal with post request that don't contain thr right data
            data =request.POST
            sender_id=data['sender_id']
            receiver_id = data['receiver_id']
            msg_content=data['msg_content']
            print msg_content
            # user=User.objects.filter(username=sender_username)
            # sender_id=user[0].id
            # user=User.objects.filter(username=receiver_username)
            # receiver_id=user[0].id
            message= Message(sender_id=sender_id,receiver_id=receiver_id,msg_content=msg_content)
            response = JSONResponse("{'done:done'}")
            _acao_response(response)
            return response
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
