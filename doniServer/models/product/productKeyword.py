from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone
from .productCategory import ProductCategory


class ProductKeyword(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=100, blank=False, unique=True)
    category = models.ForeignKey(ProductCategory, default=None, blank=True, null=True, related_name='keywords')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='keyword_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='keyword_updated_by')

    def __unicode__(self):
        return self.keyword

    class Meta:
        db_table = 'product_keywords'
        ordering = ('keyword',)

    @property
    def product_count(self):
        product_item_count = self.product_items.all().count()
        return int(product_item_count)

    def get_obj(self):
        return {
            'id': self.id,
            'name': self.keyword,
            'noOfProductItems': self.product_count,
            'categoryId': self.category.id if self.category else None,
            'categoryName': self.category.name if self.category else None
        }


from django.contrib import admin


class ProductKeywordAdmin(admin.ModelAdmin):
    model = ProductKeyword
    list_display = ('keyword', 'category', 'created_by', 'created_at')
    fieldsets = [
        ('Category Details', {'fields': ['keyword', 'category']})
    ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

