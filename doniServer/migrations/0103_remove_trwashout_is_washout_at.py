# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-12 13:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0102_trwashout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trwashout',
            name='is_washout_at',
        ),
    ]
