# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-24 08:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0055_productitem_price_on_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricemetric',
            name='kgs',
            field=models.IntegerField(null=True),
        ),
    ]