# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-13 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20170413_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visitors',
            field=models.IntegerField(default=0),
        ),
    ]