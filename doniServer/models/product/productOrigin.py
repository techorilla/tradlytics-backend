

from django.db import models
from django_countries.fields import CountryField
from .products import Products




class ProductOrigin(models.Model):
    country = CountryField(blank_label='(select country)', null=False)
    product = models.ForeignKey(Products, null=False, related_name='countries')


    class Meta:
        ordering = ['product', 'country']
        unique_together = ('product', 'country',)

    @property
    def product_items(self):
        return list(self.origin_product_item.all())

    @property
    def get_product_items_price_on_web(self):
        product_items=self.origin_product_item.filter(price_on_website=True).order_by('price_on_website_order')
        return product_items

    @property
    def get_product_items(self):
        product_items = self.origin_product_item.all()
        return [item.get_dropdown() for item in product_items]

    def __unicode__(self):
        return '(%s:%s)' % (self.product.name, str(self.country.name))

from django.contrib import admin


class ProductOriginAdmin(admin.ModelAdmin):
    list_display = ('product', 'country')
    search_fields = ['product__name']
