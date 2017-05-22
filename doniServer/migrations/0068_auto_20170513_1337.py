# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-13 13:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0067_auto_20170513_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trcommission',
            name='transaction',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='commission', serialize=False, to='doniServer.Transaction'),
        ),
    ]