# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-14 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0017_auto_20170107_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='bpbasic',
            name='bp_admin',
            field=models.BooleanField(default=False),
        ),
    ]