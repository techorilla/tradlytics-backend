# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-12 10:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import doniServer.fields.var_binary


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0141_transactionshipmenttracking'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doniLocalTrade', '0008_auto_20170811_0900'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalFiles',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=400, null=True)),
                ('file', doniServer.fields.var_binary.VarBinaryField()),
                ('extension', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='local_file_created_by', to=settings.AUTH_USER_MODEL)),
                ('local_trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='local_trade_files', to='doniServer.Transaction')),
            ],
            options={
                'db_table': 'local_tr_files',
            },
        ),
    ]
