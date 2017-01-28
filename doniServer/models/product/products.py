from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from ..businessPartner.bpBasic import BpBasic
from django.conf import settings
from django.db.models import Q
import os
import time


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True)
    business = models.ForeignKey(BpBasic, default=BpBasic.get_admin_business().bp_id)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='product_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='product_updated_by')

    class Meta:
        db_table = 'product'

    def __unicode__(self):
        return self.name

    def get_product_list_obj(self, base_url):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.get_product_image(base_url)
        }

    def get_product_image(self, base_url):
        pre = 'https://' if settings.IS_HTTPS else 'http://'
        try:
            product_image = self.productimages_set.filter(id=self.id)[0]
            print product_image
        except Exception, e:
            print str(e)
            product_image = None
        return pre + base_url + '/media/' + str(product_image) if product_image else None


def get_image_path(instance, filename):
    return os.path.join('products', instance.product.name, str(time.time())+'_'+filename)


class ProductImages(models.Model):
    product = models.ForeignKey(Products, null=False, on_delete=models.CASCADE, related_name='product')
    image = models.ImageField(upload_to='media/products/')
    primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='prod_image_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='prod_image_updated_by')

    class Meta:
        db_table = 'product_images'

    def __unicode__(self):
        return self.image

