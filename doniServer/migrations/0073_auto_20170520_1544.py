# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-20 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0072_shippingline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vessel',
            name='image',
        ),
        migrations.AddField(
            model_name='shippingline',
            name='code_name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='operator',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
