# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-02 08:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('doniServer', '0135_auto_20170731_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartialShipments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_shipment', to='doniServer.Transaction')),
                ('transaction', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partial_shipment', to='doniServer.Transaction')),
            ],
            options={
                'db_table': 'transaction_partial_shipment',
            },
        ),
        migrations.RenameModel(
            old_name='PrimaryTrade',
            new_name='SeacondaryTrades',
        ),
        migrations.AddField(
            model_name='trshipment',
            name='container_no',
            field=jsonfield.fields.JSONField(null=True),
        ),
        migrations.AlterModelTable(
            name='seacondarytrades',
            table='transaction_secodary_trades',
        ),
    ]