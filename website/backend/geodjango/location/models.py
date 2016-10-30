from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Location(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    locationName = models.CharField(max_length=200, blank=True, default='')
    xcoordinate = models.DecimalField(max_digits=8, decimal_places=5, default=0.00)
    ycoordinate = models.DecimalField(max_digits=8, decimal_places=5, default=0.00)

    class Meta:
        ordering = ('created',)
