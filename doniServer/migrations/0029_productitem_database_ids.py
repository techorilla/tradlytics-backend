# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0028_auto_20170307_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='productitem',
            name='database_ids',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
