# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 14:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0026_auto_20170306_1422'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productorigin',
            unique_together=set([('product', 'country')]),
        ),
    ]
