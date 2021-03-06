# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0053_products_on_website'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyExchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_code_in', models.CharField(max_length=3)),
                ('currency_code_out', models.CharField(max_length=3)),
                ('exchange_rate', models.FloatField()),
                ('exchange_rate_on', models.DateField()),
            ],
            options={
                'ordering': ['-exchange_rate_on'],
                'db_table': 'currency_exchange',
            },
        ),
    ]
