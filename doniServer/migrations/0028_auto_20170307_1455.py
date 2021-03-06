# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0027_auto_20170307_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productkeyword',
            name='keyword',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='productkeyword',
            unique_together=set([('keyword', 'category')]),
        ),
    ]
