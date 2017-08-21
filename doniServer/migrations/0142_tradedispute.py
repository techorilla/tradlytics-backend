# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-16 12:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doniServer', '0141_transactionshipmenttracking'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeDispute',
            fields=[
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='dispute', serialize=False, to='doniServer.Transaction')),
                ('quality_complain', models.BooleanField(default=False)),
                ('weight_shortage', models.BooleanField(default=False)),
                ('other', models.BooleanField(default=False)),
                ('other_complain', models.BooleanField(default=False)),
                ('dispute_resolved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tr_dispute_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tr_dispute_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tr_dispute',
            },
        ),
    ]
