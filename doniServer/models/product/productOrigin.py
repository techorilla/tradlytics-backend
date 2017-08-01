

from django.db import models
from django_countries.fields import CountryField
from .products import Products
from django.conf import settings




class ProductOrigin(models.Model):
    country = CountryField(blank_label='(select country)', null=False)
    product = models.ForeignKey(Products, null=False, related_name='countries')
    country_name = models.CharField(max_length=200, null=True)
    country_flag = models.CharField(max_length=100, null=True)


    class Meta:
        ordering = ['product', 'country']
        unique_together = ('product', 'country',)

    def save(self):
        self.country_name=self.country.name
        self.country_flag=self.country.flag
        super(ProductOrigin, self).save()

    @classmethod
    def re_save_all_product_origin(cls):
        product_origin = cls.objects.all()
        for origin in product_origin:
            origin.save()


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
