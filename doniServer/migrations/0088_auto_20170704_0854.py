# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-04 08:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0087_trshipment_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trshipment',
            name='actual_arrived',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='trshipment',
            name='date_arrived',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='trshipment',
            name='expected_arrival',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='trshipment',
            name='expected_shipment',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='trshipment',
            name='in_transit',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='trshipment',
            name='invoice_no',
            field=models.CharField(max_length=50, null=True),
        ),
    ]