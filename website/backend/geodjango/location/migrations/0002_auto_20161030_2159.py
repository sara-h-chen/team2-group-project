# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='xcoordinate',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=8),
        ),
        migrations.AddField(
            model_name='location',
            name='ycoordinate',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=8),
        ),
    ]
