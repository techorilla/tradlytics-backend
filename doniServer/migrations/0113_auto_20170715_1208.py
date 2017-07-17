# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-15 12:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0112_auto_20170715_1005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trcommission',
            old_name='earned_commission',
            new_name='actual_commission',
        ),
        migrations.RenameField(
            model_name='trcommission',
            old_name='net_commission',
            new_name='buyer_broker_commission_actual',
        ),
        migrations.AddField(
            model_name='transaction',
            name='quantity_fcl',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='trcommission',
            name='buyer_broker_commission_expected',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='trcommission',
            name='expected_commission',
            field=models.FloatField(default=0.0),
        ),
    ]
