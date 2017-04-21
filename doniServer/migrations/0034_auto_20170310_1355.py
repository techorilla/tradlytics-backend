# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 13:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doniServer', '0033_auto_20170310_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPriceMetric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_metric_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='price_metric_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'price_metric',
            },
        ),
        migrations.AddField(
            model_name='products',
            name='product_code',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
