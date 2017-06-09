from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class ShippingPort(models.Model):

    country = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    lo_code = models.CharField(max_length=300, null=False)
    location = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=100)
    website = models.CharField(max_length=300)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='ship_port_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='ship_port_updated_by')

    def __unicode__(self):
        return '%s:%s:%s'%(self.country, self.name, self.lo_code)



