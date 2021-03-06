# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-20 13:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doniServer', '0009_contactus_business'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=b'media/products/')),
                ('primary', models.BooleanField(default=False)),
                ('cropping', image_cropping.fields.ImageRatioField(b'image', '430x360', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod_image_created_by', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='doniServer.Products')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prod_image_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'product_images',
            },
        ),
        migrations.RemoveField(
            model_name='productimages',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='productimages',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productimages',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='ProductImages',
        ),
    ]
