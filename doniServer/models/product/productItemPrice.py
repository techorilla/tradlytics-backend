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

    @property
    def get_market_current_price(self):
        price_items = self.price_items
        price = [item.get('priceValue') for item in price_items if item.get('currentValue')]
        price = price[0]
        return price

    @classmethod
    def get_all_prices(cls, start_time, end_time):
        price_items = cls.objects.filter(price_time__gte=start_time, price_time__lte=end_time)
        price_items = [item.get_obj() for item in price_items]
        return price_items

    def get_obj(self):
        price_item = {
            'id': self.id,
            'showDetails': False,
            'product': self.product_item.product_origin.product.name,
            'productId': self.product_item.product_origin.product.id,
            'priceMarketId': self.price_market.id,
            'productName': self.product_item.product_origin.product.name,
            'productItemId': self.product_item.id,
            'priceItems': self.price_items,
            'priceTime': self.price_time,
            'comments': self.comments,
            'keywords': self.product_item.keyword_str,
            'productOriginName': self.product_item.product_origin.country.name,
            'productOriginFlag': self.product_item.product_origin.country.flag,
            'marketCurrency': self.price_market.currency,
            'marketCountry': self.price_market.country_name,
            'currentPrice': self.get_market_current_price,
            'updatedBy': self.updated_by.username if self.updated_by else None,
            'updatedAt': self.updated_at,
            'createdBy': self.created_by.username if self.created_by else None,
            'createdAt': self.created_at
        }
        return price_item
