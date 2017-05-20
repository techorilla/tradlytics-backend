from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from ..businessPartner.bpBasic import BpBasic
from django.conf import settings
from .productCategory import ProductCategory
from django.db.models import Q
import os
import time
from django_countries.fields import CountryField


def get_image_path(instance, filename):
    return os.path.join('products', str(time.time())+'_'+instance.name+'_'+filename)


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    description = models.TextField(null=True)
    on_website = models.BooleanField(default=False)
    product_code = models.CharField(max_length=10, null=True, unique=True)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, related_name='products')
    related_products = models.ManyToManyField('self', blank=True, null=True, related_name='related_products')
    business = models.ForeignKey(BpBasic, default=BpBasic.get_admin_business().bp_id)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='product_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='product_updated_by')

    class Meta:
        db_table = 'product'

    def __unicode__(self):
        return self.name

    def get_tag(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.name
        }

    def get_obj(self, base_url):
        return {
            'id': self.id,
            'info':{
                'relatedProduct': [prod.get_tag() for prod in self.related_products.all()],
                'onWebsite': self.on_website,
                'id': self.id,
                'name': self.name,
                'productCode': self.product_code,
                'image': self.get_product_image(base_url),
                'description': self.description,
                'categoryId': self.category.id if self.category else None,
                'categoryName': self.category.name if self.category else 'No Category Defined',
            },
            'isDeletable': self.is_deletable,
            'origins': self.product_origins,
            'productItems': self.product_items_obj,
            'updatedBy': self.updated_by.username if self.updated_by else None,
            'updatedAt': self.updated_at,
            'createdBy': self.created_by.username,
            'createdAt': self.created_at
        }

    @property
    def is_deletable(self):
        manifest_count = self.product_manifest.count()
        product_item_count = len(self.product_items)
        return (manifest_count == 0) and (product_item_count == 0)

    @property
    def related_product_names(self):
        related_product_names = self.related_products.all().values('name')
        related_product_names = [prod.get('name') for prod in related_product_names]
        return ', '.join(related_product_names)


    @property
    def related_product_ids(self):
        related_product_ids = self.related_products.all().values('id')
        return [prod.get('id') for prod in related_product_ids]

    @property
    def product_origins(self):
        origins = self.countries.all()
        origins = [origin.country.code for origin in origins]
        return origins

    @property
    def product_items_obj(self):
        product_items = []
        product_origin = self.countries.all()
        for product in product_origin:
            product_items = product_items + product.get_product_items
        return product_items


    @property
    def product_items(self):
        product_items = []
        product_origin = self.countries.all()
        for product in product_origin:
            product_items = product_items + product.product_items
        return product_items

    @classmethod
    def get_products_for_website(cls, base_url):
        products = cls.objects.filter(on_website=True).order_by('name')
        return [product.get_product_list_obj(base_url, website=True) for product in products]

    @classmethod
    def get_dropdown(cls):
        products = cls.objects.all().order_by('name')
        products = [{
            'id': prod.id,
            'name': prod.name,
            'category': 'No Category Entered' if prod.category is None else prod.category.name
        } for prod in products]
        return products

    @property
    def origins(self):
        return self.countries.all()

    def get_product_list_obj(self, base_url, website=False):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.get_product_image(base_url),
            'category': self.category if website else self.category.name if self.category else None
        }

    def get_product_single_website(self, base_url):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.get_product_image(base_url),
            'category': self.category
        }

    def get_product_image(self, base_url):
        pre = 'https://' if settings.IS_HTTPS else 'http://'
        return pre + base_url + '/media/' + str(self.image) if self.image else None

#
# def get_image_path(instance, filename):
#     return os.path.join('products', instance.product.name, str(time.time())+'_'+filename)
#
#
# class ProductImage(models.Model):
#     product = models.ForeignKey(Products, null=False, on_delete=models.CASCADE, related_name='product_images')
#     image = models.ImageField(upload_to='media/products/')
#     primary = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(default=None, null=True)
#     created_by = models.ForeignKey(User, null=False, blank=False, related_name='prod_image_created_by')
#     updated_by = models.ForeignKey(User, null=True, blank=False, related_name='prod_image_updated_by')
#
#     class Meta:
#         db_table = 'product_images'
#
#     def __unicode__(self):
#         return str(self.image)
#
#
#
#
# from django.contrib import admin
#
#
# class ProductImageInline(admin.StackedInline):
#     classes = ('grp-collapse grp-open',)
#     inline_classes = ('grp-collapse grp-open',)
#     model = ProductImage
#     exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')
#     extra = 1
#
#
# class ProductAdmin(admin.ModelAdmin):
#     model = Products
#     list_display = ('name', 'product_code', 'description', 'category')
#     fieldsets = [
#         ('Product Details', {'fields': ['name', 'description', 'product_code']}),
#         ('Product Category', {'fields': ['category']})
#     ]
#     inlines = [ProductImageInline]
#
#     def save_formset(self, request, form, formset, change):
#         def set_user(instance):
#             if not hasattr(instance, 'created_by'):
#                 instance.created_by = request.user
#             else:
#                 instance.updated_by = request.user
#             instance.save()
#         print formset
#         instances = formset.save(commit=False)
#         print list(instances)
#         map(set_user, instances)
#         return instances
#
#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user
#             obj.business = request.user.profile.business
#         else:
#             obj.updated_by = request.user
#         obj.save()
#         return obj
#
#





