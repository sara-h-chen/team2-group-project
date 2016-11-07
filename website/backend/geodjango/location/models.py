from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Location(models.Model):
    owner = models.ForeignKey('auth.User', related_name='location', default='')
    created = models.DateTimeField(auto_now_add=True)
    locationName = models.CharField(max_length=200, blank=True, default='')
    xcoordinate = models.DecimalField(max_digits=8, decimal_places=5, default=0.00)
    ycoordinate = models.DecimalField(max_digits=8, decimal_places=5, default=0.00)

    class Meta:
        ordering = ('created',)

def save(self, *args, **kwargs):
    options = self.locationName and {'Location Name': self.locationName} or {}
    ycoordinate = self.ycoordinate and 'table' or False
    xcoordinate = self.xcoordinate and 'table' or False
    super(Location, self).save(*args, **kwargs)

class Test(models.Model):
    ratings = ((1,1),(2,2),(3,3),(4,4),(5,5))
    userNumber = models.AutoField(primary_key=True)
    name = models.CharField('Name', max_length=200)
    location = models.FloatField("Location")
    rating = models.IntegerField(choices = ratings)

class UserDB(models.Model):
    name = models.CharField(max_length=200)
    longditude = models.FloatField()
    latitude = models.FloatField()
    one = 1
    two = 2
    three = 3
    four = 4
    five=5
    RATING_CHOICES = (
        (one, 'One'),
        (two, 'Two'),
        (three, 'Three'),
        (four, 'Four'),
        (five, 'Five'),
    )
    user_rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=three,
    )
