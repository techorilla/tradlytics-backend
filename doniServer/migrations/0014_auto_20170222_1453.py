# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0013_productorigin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productorigin',
            options={'ordering': ['product', 'country']},
        ),
        migrations.AlterField(
            model_name='productorigin',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='countries', to='doniServer.Products'),
        ),
    ]