# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-13 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_post_display_on_web'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateField(default=None, null=True),
        ),
    ]