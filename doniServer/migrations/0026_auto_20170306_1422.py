# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0025_auto_20170306_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_users', to='doniServer.BpBasic'),
        ),
    ]