from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework import generics

from backend.models import User, Food
from backend.serializers import FoodSerializer

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
    output='search'
    return HttpResponse(output)

def search(request):
    output='notifcation'
    return HttpResponse(output)
# GETS THE USERNAME FROM THE URL AS A PARAM
def user_page(request, username):
    # GET PARTICULAR USER FROM DB BASED ON PARAM
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404('Requested user not found.')
    # food = user.product_set.all()
    # template = loader.get_template('pagehere.html')
    # variables = Context({
    #     'username': username,
    #     'food': food
    # })
    # output = template.render(variables)
    # return HttpResponse(output)

# TEMPLATE PAGES ARE JUST PLAIN HTML DOCS AND SHOULD FOLLOW THIS FORMAT #
#########################################################################
#     < html >                                                          #
#     < head >                                                          #
#     < title > Django                                                  #
#     product - User: {{username}} < / title >                          #
#     < / head >                                                        #
#     < body >                                                          #
#     < h1 > product                                                    #
#     for {{username}} </ h1 >                                          #
#     { % if product %}                                                 #
#     < ul >                                                            #
#     { % for prod in product %}                                        #
#     < li > < a href = "{{ product.link.url }}" >                      #
#     {{product.title}} < / a > < / li >                                #
#     { % endfor %}                                                     #
#     < / ul >                                                          #
#     { % else %}                                                       #
#     < p > No product found. < / p >                                   #
#     { % endif %}                                                      #
#     < / body >                                                        #
#     < / html >                                                        #

#########################################################################
#                VIEWS USING CLASS-BASED DJANGO REST                    #
#########################################################################
class FoodList(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
