from django.db import models
from django.contrib.auth.models import User
from .products import Products
from datetime import date
from django.utils import timezone


class ProductPrice(models.Model):
    product = models.ForeignKey(Products, null=False, )
    local_price = models.FloatField(default=0.00)
    international_price = models.FloatField(default=0.00)
    date = models.DateField(default=date.today)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='product_price_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='product_price_updated_by')

    class Meta:
        db_table = 'product_price'

    def __unicode__(self):
        return self.name
