from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from rest_framework import status, renderers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken import views as auth_views
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token

from serializers import *
from models import Food, Message
from permissions import IsOwnerOrReadOnly

##########################################################
#                      HEADER CONTROL                    #
##########################################################


def _acao_response(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'


def _options_allow_access():
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
    response['Access-Control-Max-Age'] = 1000
    # note that '*' is not valid for Access-Control-Allow-Headers
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, ' \
                                               'X-Requested-With, origin, x-csrftoken, ' \
                                               'content-type, accept'
    return response


#########################################################
#               AUTHENTICATION METHOD                   #
#########################################################

# Takes the place of the login mechanism
# Extends parent class to produce token cookies
class ObtainAuthToken(auth_views.ObtainAuthToken):
    parser_classes = (FormParser, MultiPartParser, JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def options(self, request, *args, **kwargs):
        return _options_allow_access()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response = JSONResponse({'token': token.key})
        _acao_response(response)
        response.set_cookie('auth-token', token.key)
        return response

obtain_auth_token = ObtainAuthToken.as_view()


#########################################################
#                USER-RELATED QUERIES                   #
#########################################################


@csrf_exempt
@api_view(['GET', 'POST', 'OPTIONS'])
# Create user through POST request
def createUser(request):
    if request.method == 'OPTIONS':
        return _options_allow_access()
    if request.method == 'POST':
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = HttpResponse(status=status.HTTP_201_CREATED)
            _acao_response(response)
            return response
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


def identify(request, user_id):
    try:
        user=User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        response = JSONResponse(serializer.data)
        _acao_response(response)
        return response
    except:
        response = HttpResponse('User not found')
        _acao_response(response)
        return response


#########################################################
#                FOOD-RELATED QUERIES                   #
#########################################################

# UNUSED: RETURNS FOOD LISTING (for reference only!)
# def food_listing(request):
#     latest_food_requests = Food.objects.order_by('Date listed')
#     output = ', '.join([food.food_name for food in latest_food_requests])
#     return HttpResponse(output)

@api_view(['GET', 'POST', 'OPTIONS'])
def foodListHandler(request, latitude, longitude):
    """
    Deals with incoming OPTIONS for FOODLIST functions
    """
    if request.method == 'OPTIONS':
        return _options_allow_access()
    else:
        foodList(request, latitude, longitude)


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def foodList(request, latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)
    if request.method == 'OPTIONS':
        return _options_allow_access()

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
            response = JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
            _acao_response(response)
            return response
        response = JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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


@api_view(['PUT', 'DELETE', 'OPTIONS'])
def updateHandler(request, id):
    """
    Deals with incoming OPTIONS for UPDATE functions
    """
    if request.method == 'OPTIONS':
        return _options_allow_access()
    else:
        update(request, id)


@csrf_exempt
@api_view(['PUT', 'DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated, IsOwnerOrReadOnly,))
def update(request, id):
    try:
        foodItem = Food.objects.get(id=id)
    except Food.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = FoodSerializer(foodItem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return _acao_response(HttpResponse(status=status.HTTP_200_OK))
        return _acao_response(JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST))

    elif request.method == 'DELETE':
        foodItem.delete()
        return _acao_response(HttpResponse(status=status.HTTP_204_NO_CONTENT))



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
        messageList = Message.objects.filter(Q(receiver_id=uID) | Q(sender_id=uID))
        serializer = MessageSerializer(messageList, many=True)
        response = JSONResponse(serializer.data)
        _acao_response(response)
        return response
    except Message.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except IndexError:
        response = HttpResponse('User not found')
        _acao_response(response)
        return response

@csrf_exempt
def getMessagesBetween(request):
    try:
        if request.method == "POST":
            data= request.POST
            userA=data['userA']
            userB = data['userB']
            print userA,userB
            messageList = Message.objects.filter((Q(receiver_id=userA) & Q(sender_id=userB)) | (Q(receiver_id=userB) & Q(sender_id=userA)))
            serializer = MessageSerializer(messageList, many=True)
            response = JSONResponse(serializer.data)
            response['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
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
        _acao_response(response)
        return response
    except Message.DoesNotExist:
        response = HttpResponse(status=status.HTTP_404_NOT_FOUND)
        _acao_response(response)
        return response
    except IndexError:
        response = HttpResponse('User not found')
        _acao_response(response)
        return response

@csrf_exempt
def addMessage(request, username):
    try:
        if request.method == "POST":#TODO make robust i.e. deal with post request that don't contain thr right data
            data =request.POST
            sender_id=data['sender_id']
            receiver_id = data['receiver_id']
            msg_content=data['msg_content']
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
