# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0044_auto_20170320_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='bpbank',
            name='acc_city',
            field=models.CharField(max_length=200, null=True),
        ),
    ]