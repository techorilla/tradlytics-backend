# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 13:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0012_auto_20170222_0759'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOrigin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doniServer.Products')),
            ],
        ),
    ]
