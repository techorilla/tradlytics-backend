# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 12:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0043_auto_20170320_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bpbank',
            name='bp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banks', to='doniServer.BpBasic'),
        ),
    ]
