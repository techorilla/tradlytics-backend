# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-04 08:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0086_auto_20170615_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='trshipment',
            name='transaction',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='doniServer.Transaction'),
        ),
    ]
