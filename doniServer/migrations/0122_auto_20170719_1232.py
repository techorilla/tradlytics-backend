# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-19 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0121_trcomplete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trshipment',
            name='not_shipped_reason',
            field=models.TextField(null=True),
        ),
    ]
