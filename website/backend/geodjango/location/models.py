from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Location(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    locationName = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        ordering = ('created',)
