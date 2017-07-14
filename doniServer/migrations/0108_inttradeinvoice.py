# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-14 13:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doniServer', '0107_auto_20170714_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntTradeInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_date', models.DateField(default=None)),
                ('invoice_no', models.IntegerField()),
                ('invoice_obj', jsonfield.fields.JSONField()),
                ('invoice_amount', models.FloatField(default=0.0)),
                ('weight_in_kg', models.FloatField(default=0.0)),
                ('rate_per_kg', models.FloatField(default=0.0)),
                ('currency', models.CharField(default=b'PKR', max_length=20)),
                ('note', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_created_by', to=settings.AUTH_USER_MODEL)),
                ('transaction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='invoices', to='doniServer.Transaction')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
