# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-14 06:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0002_auto_20170214_0633'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductsCategory',
            new_name='ProductCategory',
        ),
    ]
