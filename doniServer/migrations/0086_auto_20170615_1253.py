# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-15 12:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0085_auto_20170615_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='business',
            field=models.ForeignKey(default=1L, on_delete=django.db.models.deletion.CASCADE, to='doniServer.BpBasic'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='business',
            field=models.ForeignKey(default=1L, on_delete=django.db.models.deletion.CASCADE, to='doniServer.BpBasic'),
        ),
        migrations.AlterField(
            model_name='products',
            name='business',
            field=models.ForeignKey(default=1L, on_delete=django.db.models.deletion.CASCADE, to='doniServer.BpBasic'),
        ),
    ]
