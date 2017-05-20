from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

def get_image_path(instance, filename):
    return os.path.join('shippingLine', str(instance.name+'_'+filename))

class ShippingLine(models.Model):
    code_name = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=300, null=False)
    website = models.CharField(max_length=300, null=True)
    logo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='shipping_line_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='shipping_line_updated_by')