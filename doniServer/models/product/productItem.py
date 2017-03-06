from .products import Products
from django.contrib.auth.models import User
from .productKeyword import ProductKeyword
from .productOrigin import ProductOrigin
from django.db import models

from django.utils import timezone
from django.contrib import admin


class ProductItem(models.Model):
    keywords = models.ManyToManyField(ProductKeyword, related_name='product_items')
    product_origin = models.ForeignKey(ProductOrigin, null=True, blank=False, related_name='origin_product_item')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='prod_item_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='prod_item_updated_by')

    def get_dropdown(self):
        return {
            'id': self.id,
            'name': self.product_origin.product.name,
            'origin': self.product_origin.country.name,
            'keywords': self.keyword_str
        }

    @property
    def keywords_ids(self):
        keywords = self.keywords.all()
        print keywords
        return [key.id for key in keywords]

    @property
    def keyword_str(self):
        keywords = self.keywords.all()
        keywords = [str(key.keyword) for key in keywords]
        return ', '.join(keywords)


    def get_obj(self):
        return {
            'id': self.id,
            'productId': self.product_origin.product.id,
            'productName': self.product_origin.product.name,
            'origin': self.product_origin.country.code.upper(),
            'productOriginName': self.product_origin.country.name,
            'productOriginFlag': self.product_origin.country.flag,
            'keywords': self.keywords_ids,
            'keywordsString': self.keyword_str,
            'updatedBy': self.updated_by.username if self.updated_by else None,
            'updatedAt': self.updated_at,
            'createdBy': self.created_by.username,
            'createdAt': self.created_at
        }


class ProductItemAdmin(admin.ModelAdmin):
    model = Products
    list_display = ('product_origin',)


