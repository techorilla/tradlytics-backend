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


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, related_name='products')
    business = models.ForeignKey(BpBasic, default=BpBasic.get_admin_business().bp_id)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='product_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='product_updated_by')

    class Meta:
        db_table = 'product'

    def __unicode__(self):
        return self.name

    def get_obj(self, base_url):
        return {
            'id': self.id,
            'info':{
                'id': self.id,
                'name': self.name,
                'image': self.get_product_image(base_url),
                'description': self.description,
                'categoryId': self.category.id if self.category else None,
                'categoryName': self.category.name if self.category else 'No Category Defined',

            },
            'origins': self.product_origins,
            'productItems': self.product_items,
            'updatedBy': self.updated_by.username if self.updated_by else None,
            'updatedAt': self.updated_at,
            'createdBy': self.created_by.username,
            'createdAt': self.created_at
        }

    @property
    def product_origins(self):
        origins = self.countries.all()
        origins = [origin.country.code for origin in origins]
        return origins

    @property
    def product_items(self):
        product_items = []
        product_origin = self.countries.all()
        for product in product_origin:
            print product.get_product_items
            product_items = product_items + product.get_product_items
        return product_items

    @classmethod
    def get_products_for_website(cls, base_url):
        products = cls.objects.all().order_by('name')
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
        try:
            product_image = self.product_images.filter(primary=True).order_by('-created_by')[0]
        except Exception, e:
            product_image = None
        return pre + base_url + '/media/' + str(product_image) if product_image else None


def get_image_path(instance, filename):
    return os.path.join('products', instance.product.name, str(time.time())+'_'+filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Products, null=False, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='media/products/')
    primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='prod_image_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='prod_image_updated_by')

    class Meta:
        db_table = 'product_images'

    def __unicode__(self):
        return str(self.image)




from django.contrib import admin


class ProductImageInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    model = ProductImage
    exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    model = Products
    list_display = ('name', 'description', 'category')
    fieldsets = [
        ('Product Details', {'fields': ['name', 'description']}),
        ('Product Category', {'fields': ['category']})
    ]
    inlines = [ProductImageInline]

    def save_formset(self, request, form, formset, change):
        def set_user(instance):
            if not hasattr(instance, 'created_by'):
                instance.created_by = request.user
            else:
                instance.updated_by = request.user
            instance.save()
        print formset
        instances = formset.save(commit=False)
        print list(instances)
        map(set_user, instances)
        return instances

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.business = request.user.profile.business
        else:
            obj.updated_by = request.user
        obj.save()
        return obj







