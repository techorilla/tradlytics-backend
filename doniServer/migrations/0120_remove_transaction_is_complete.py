# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-18 15:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0119_auto_20170718_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='is_complete',
        ),
    ]