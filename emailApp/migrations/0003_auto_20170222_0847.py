# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 08:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailApp', '0002_auto_20170222_0832'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailmessage',
            old_name='emailbody',
            new_name='body',
        ),
    ]
