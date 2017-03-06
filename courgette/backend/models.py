from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.username

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
    # location = models.CharField(max_length=200,default='Durham')
    # picture = models.FileField(upload_to='images/%Y/%m/%d')
    user = models.ForeignKey(User,default="root",on_delete=models.CASCADE)

    def __str__(self):
        return self.food_name + " " + self.quantity



class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender")
    receiver = models.ForeignKey(User, related_name="receiver")
    msg_content = models.TextField
    created_at = models.TimeField
    read = models.BooleanField
