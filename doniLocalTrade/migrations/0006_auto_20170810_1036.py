# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-10 10:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doniLocalTrade', '0005_localtradestatus_completion_status_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='localtrade',
            old_name='buyer',
            new_name='local_buyer',
        ),
        migrations.RenameField(
            model_name='localtrade',
            old_name='seller',
            new_name='local_seller',
        ),
    ]
