# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-04 21:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0091_transactionchangelog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionchangelog',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='change_log', to='doniServer.Transaction'),
        ),
    ]
