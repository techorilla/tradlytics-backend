from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
import time
import os


def get_image_path(instance, filename):
    return os.path.join('shippingLine', instance.name, str(time.time())+'_'+filename)


class ShippingLine(models.Model):
    code_name = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=300, null=False)
    website = models.CharField(max_length=300, null=True)
    tracking_website = models.CharField(max_length=300, null=True)
    logo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='shipping_line_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='shipping_line_updated_by')


    def get_complete_obj(self, base_url):
        return {
            'id': self.id,
            'name': self.name,
            'codeName': self.code_name,
            'website': self.website,
            'logo': self.get_line_logo(base_url),
            'createdBy': self.created_by.username,
            'createdOn': self.created_at
        }

    def get_list_obj(self, base_url):
        return {
            'id': self.id,
            'name': self.name,
            'codeName': self.code_name,
            'website': self.website,
            'logo': self.get_line_logo(base_url),
            'vesselCount': self.vessels.count()
        }

    def get_drop_down_obj(self):
        return {
            'id': self.id,
            'name': self.name,
            'codeName': self.code_name
        }




    def get_obj(self, base_url):
        return {
            'id': self.id,
            'name': self.name,
            'codeName': self.code_name,
            'website': self.website,
            'logo': self.get_line_logo(base_url),
            'createdBy': self.created_by.username,
            'createdOn': self.created_at
        }

    def get_line_logo(self, base_url):
        if settings.IS_HTTPS:
            pre = 'https://'
        else:
            pre = 'http://'
        return pre+base_url+'/media/'+str(self.logo) if self.logo else None
