# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-20 07:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doniLocalTrade', '0013_auto_20170905_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localtrade',
            name='international_file',
        ),
    ]
