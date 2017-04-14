from django.db import models
from django.contrib.auth.models import User
from .productItem import ProductItem
from datetime import date
from django.utils import timezone
from .priceMarket import PriceMarket
from jsonfield import JSONField


class ProductPrice(models.Model):
    product_item = models.ForeignKey(ProductItem, default=None, null=False, related_name='product_item_price')
    product_market = models.ForeignKey(PriceMarket, null=True, default=None)
    price_value = models.FloatField(default=0.00)
    price_on = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='product_price_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='product_price_updated_by')

    class Meta:
        db_table = 'product_price'

    def __unicode__(self):
        return self.name


class Price(models.Model):
    price_metric = models.CharField(max_length=50, choices=[('MT', 'mt'), ('Kg', 'kg')])
    price_value = models.FloatField(default=0.00)
    shipment = models.DateField()
    show_on_ticker = models.BooleanField(default=False)
    show_on_pricing = models.BooleanField(default=False)
    product_price = models.ForeignKey(ProductPrice, null=False)


from django.contrib import admin

class ProductPriceAdmin(admin.ModelAdmin):
    model = ProductPrice
    # formfield_overrides = {
    #     JSONField: {'widget': JSONEditor},
    # }
    # fieldsets = [
    #     ('Product Details', {'fields': ['product', 'product_keywords', ]}),
    #     ('Product Specification', {'fields': ['product_specs_data']}),
    #     ('Price Details', {'fields': ['product_market', 'price_value', 'price_on']})
    # ]
    #
    # filter_horizontal = 'product_keywords',
    #
    # def save_model(self, request, obj, form, change):
    #     print obj
    #     print request
    #     obj.created_by = request.user
    #     obj.save()





