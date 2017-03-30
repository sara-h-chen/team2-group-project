import json

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase

from models import Food

# Create your tests here.
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
        user = User.objects.get(username='plato')
        response = self.client.post('/food/1.0/1.0', json.dumps(data), content_type='application/json')
        force_authenticate(response, user=user, token=user.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)



##########################################################
#                   FOOD UPDATING TEST                   #
##########################################################