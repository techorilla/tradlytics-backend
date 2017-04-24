# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-24 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0059_productitem_import_expense'),
    ]

    operations = [
        migrations.AddField(
            model_name='productitemprice',
            name='current_price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='productitemprice',
            name='rs_per_kg',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='productitemprice',
            name='usd_per_pmt',
            field=models.FloatField(null=True),
        ),
    ]
