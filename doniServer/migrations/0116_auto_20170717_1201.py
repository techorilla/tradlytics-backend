# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-17 12:01
from __future__ import unicode_literals

from django.db import migrations
import doniServer.fields.var_binary


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0115_auto_20170717_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trfiles',
            name='file',
            field=doniServer.fields.var_binary.VarBinaryField(max_length=b'65535'),
        ),
    ]
