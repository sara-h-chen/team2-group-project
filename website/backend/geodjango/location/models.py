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
