from django.contrib.auth.models import User
from django.db import models
from .productItem import ProductItem
from .priceMarket import PriceMarket
from django.utils import timezone
from django.contrib import admin
from jsonfield import JSONField


class ProductItemPrice(models.Model):
    id = models.AutoField(primary_key=True)
    product_item = models.ForeignKey(ProductItem, null=False, related_name='price_product_item')
    price_market = models.ForeignKey(PriceMarket, null=False, related_name='price_market')
    price_time = models.DateTimeField(default=timezone.now, db_index=True)
    price_items = JSONField(null=False)
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='prod_item_price_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='prod_item_price_updated_by')

    class Meta:
        db_table = 'product_item_price'
        ordering = ('-price_time',)
