from django.db import models
from django.contrib.auth.models import User
from .products import Products
from .productCategory import ProductCategory
from .productKeyword import ProductKeyword
from datetime import date
from django.utils import timezone
from .priceMarket import PriceMarket
from jsonfield import JSONField


class ProductPrice(models.Model):
    product = models.ForeignKey(Products, null=False, )
    product_keywords = models.ManyToManyField(ProductKeyword,
                                             blank=True,
                                             related_name='prod_keywords',
                                             db_constraint=False)

    product_specs_data = JSONField(null=True)
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


from django.contrib import admin
from jsoneditor.forms import JSONEditor


class ProductPriceAdmin(admin.ModelAdmin):
    model = ProductPrice
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
    fieldsets = [
        ('Product Details', {'fields': ['product', 'product_keywords', ]}),
        ('Product Specification', {'fields': ['product_specs_data']}),
        ('Price Details', {'fields': ['product_market', 'price_value', 'price_on']})
    ]

    filter_horizontal = 'product_keywords',

    def save_model(self, request, obj, form, change):
        print obj
        print request
        obj.created_by = request.user
        obj.save()





