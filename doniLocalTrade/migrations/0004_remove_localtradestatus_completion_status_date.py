# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-08 11:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doniLocalTrade', '0003_auto_20170808_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localtradestatus',
            name='completion_status_date',
        ),
    ]
