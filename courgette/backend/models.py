from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    food_listed = models.ForeignKey(Food, on_delete=models.CASCADE)

class Food(models.Model):
    class Meta:
        unique_together = (('food_name', 'quantity'),)
    food_name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    FOOD_TYPES = (
        (VEGETABLES, 'Vegetables'),
        (SEAFOOD, 'Seafood'),
        (MEAT, 'Meat'),
        (COOKED, 'Cooked'),
        (FRUIT, 'Fruit'),
        (BAKERY_ITEMS, 'Bakery Items'),
        (PASTA_RICE, 'Pasta & Rice'),
        (DRIED_FOOD, 'Dried food'),
        (OTHER, 'Other')
    )
    food_type = models.CharField(choices=FOOD_TYPES,default=OTHER)
    ALLERGENS = (
        (NUTS, 'Nuts'),
        (GLUTEN,'Gluten'),
        (NON_VEGAN, 'Non-Vegan'),
        (SEAFOOD, 'Seafood'),
        (EGGS, 'Eggs'),
    )
    allergens = models.CharField(allergens=ALLERGENS,default=None)
    STATUS = (
        (AVAILABLE, 'Available'),
        (RESERVED, 'Reserved'),
        (UNAVAILABLE, 'Unavailable')
    )
    status = models.CharField(status=STATUS,default=AVAILABLE)
    picture = models.FileField(upload_to='images/%Y/%m/%d')

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender")
    receiver = models.ForeignKey(User, related_name="receiver")
    msg_content = models.TextField
    created_at = models.TimeField         
