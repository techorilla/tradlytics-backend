# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-26 18:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0074_productitem_price_on_website_order'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='trfiles',
            table='tr_files',
        ),
    ]