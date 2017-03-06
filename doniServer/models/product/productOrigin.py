

from django.db import models
from django_countries.fields import CountryField
from .products import Products


class ProductOrigin(models.Model):
    country = CountryField(blank_label='(select country)', null=False)
    product = models.ForeignKey(Products, null=False, related_name='countries')

    class Meta:
        ordering = ['product', 'country']

    def __unicode__(self):
        return '(%s:%s)' % (self.product.name, str(self.country.name))

from django.contrib import admin


class ProductOriginAdmin(admin.ModelAdmin):
    list_display = ('product', 'country')
    search_fields = ['product__name']
