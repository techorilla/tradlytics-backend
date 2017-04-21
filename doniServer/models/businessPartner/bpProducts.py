from django.db import models
from datetime import date
from django.contrib.auth.models import User
from .bpBasic import BpBasic
from django.utils import timezone
from ..product import Products
import os

def get_image_path(instance, filename):
    return os.path.join('media', 'products', instance.name)


class BpProducts(models.Model):
    bp = models.ForeignKey(BpBasic,
                           null=False,
                           blank=False)

    product = models.ForeignKey(Products,
                                null=False,
                                blank=False)

    prod_image = models.ImageField(
        upload_to=get_image_path, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='bp_product_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='bp_products_updated_by')

    class Meta:
        db_table = 'bp_product'
