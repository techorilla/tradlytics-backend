# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 09:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailApp', '0003_auto_20170222_0847'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailmessage',
            old_name='baseTemplate',
            new_name='base_template',
        ),
    ]
