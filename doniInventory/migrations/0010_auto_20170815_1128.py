# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-15 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniInventory', '0009_auto_20170805_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='go_down_contact',
            field=models.CharField(default=None, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouse',
            name='go_down_keeper',
            field=models.CharField(default=None, max_length=250),
            preserve_default=False,
        ),
    ]