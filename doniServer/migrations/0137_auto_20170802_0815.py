# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-02 08:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0136_auto_20170802_0807'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='seacondarytrades',
            table='transaction_secondary_trades',
        ),
    ]
