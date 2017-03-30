import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import force_authenticate, APITestCase

from models import Food

# Create your tests here.

##########################################################
#                      HELPER CLASS                      #
##########################################################


class JSONResponse(HttpResponse):
    """
    A HttpResponse that renders content into JSON
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


##########################################################
#                   USER CREATION TEST                   #
##########################################################


class UserTests(APITestCase):
    def setUp(self):
        self.create_data = {"username": "krasus", "password": "krasus", "email": "krasus@wow.com"}

    def test_create_account(self):
        response = self.client.post(reverse('create_user'), json.dumps(self.create_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_login(self):


##########################################################
#                   FOOD POSTING TEST                    #
##########################################################
# REFER TO THIS
# user = User.objects.get(username='anduin')
# request = factory.post('/food/1.0/1.0', json.dumps({}), content_type='application/json')
# force_authenticate(request, user=user, token=user.token)
# assert response.status

# Run tests with python manage.py test

class FoodTests(APITestCase):
    def test_create_food(self):
        """
        Ensure we can create a food item
        :return:
        """

        data = {}
        user = User.objects.get(username='krasus')
        response = self.client.post('/food/1.0/1.0', json.dumps(data), content_type='application/json')
        force_authenticate(response, user=user, token=user.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)



##########################################################
#                   FOOD UPDATING TEST                   #
##########################################################