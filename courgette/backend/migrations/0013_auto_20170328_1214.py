# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20170327_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.CharField(default=b'2017-03-28 12:14:50.253444', max_length=50),
        ),
    ]
