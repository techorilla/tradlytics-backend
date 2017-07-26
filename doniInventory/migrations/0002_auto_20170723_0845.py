# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-23 08:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0129_auto_20170721_1404'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doniInventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='business_warehouse_added', to='doniServer.BpBasic'),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='created_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_created_by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouse',
            name='total_capacity_kgs',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='updated_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='inventorytransaction',
            name='transaction_business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='doniServer.BpBasic'),
        ),
    ]