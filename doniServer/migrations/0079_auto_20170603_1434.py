# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-03 14:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0078_auto_20170603_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trfiles',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='doniServer.Transaction'),
        ),
    ]
