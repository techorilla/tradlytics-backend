# from django.db import models
# from django.contrib.auth.models import User
# from ..product.products import Products
# from django.utils import timezone
# import os
#
#
# def get_image_path(instance, filename):
#     return os.path.join('media', 'products', instance.product.id, filename.split('.')[1])
#
#
# class ProductImages(models.Model):
#     product = models.ForeignKey(Products, null=False, on_delete=models.CASCADE)
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
#         return self.name
