from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):
    class Meta:
        unique_together = (('food_name', 'quantity'),)
    food_name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    date_listed = models.DateField(auto_now=True, auto_now_add=False)
    FOOD_TYPES = (
        ('VEGE', 'Vegetables'),
        ('SEAFOOD', 'Seafood'),
        ('MEAT', 'Meat'),
        ('COOKED', 'Cooked'),
        ('FRUIT', 'Fruit'),
        ('BAKERY', 'Bakery Items'),
        ('PASTA_RICE', 'Pasta & Rice'),
        ('DRIED', 'Dried food'),
        ('OTHER', 'Other')
    )
    food_type = models.CharField(choices=FOOD_TYPES,default='OTHER',max_length=50)
    ALLERGENS = (
        ('NUTS', 'Nuts'),
        ('GLUTEN','Gluten'),
        ('NON_VEGAN', 'Non-Vegan'),
        ('SEAFOOD', 'Seafood'),
        ('EGGS', 'Eggs'),
    )
    allergens = models.CharField(choices=ALLERGENS,default=None,max_length=50)
    STATUS = (
        ('AVAILABLE', 'Available'),
        ('RESERVED', 'Reserved'),
        ('UNAVAILABLE', 'Unavailable')
    )
    status = models.CharField(choices=STATUS,default='AVAILABLE',max_length=50)
    latitude = models.DecimalField(max_digits=3, decimal_places=2)
    longitude = models.DecimalField(max_digits=3, decimal_places=2)
    # picture = models.FileField(upload_to='images/%Y/%m/%d')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.food_name + " " + str(self.quantity)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender")
    receiver = models.ForeignKey(User, related_name="receiver")
    msg_content = models.CharField(max_length=500)
    created_at = models.CharField(max_length=50, default=str(datetime.now()))
    read = models.BooleanField(default=False)

    @classmethod
    def create(cls, sender, receiver, msg_content):
        message = cls(sender=sender, receiver=receiver, msg_content=msg_content)
        message.created_at = str(datetime.now())
        return message