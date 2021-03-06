# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-03 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0140_auto_20170802_1543'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionShipmentTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', jsonfield.fields.JSONField(null=True)),
                ('tracked_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipment_tracking', to='doniServer.BpBasic')),
            ],
            options={
                'db_table': 'shipment_tracking_data',
            },
        ),
    ]
