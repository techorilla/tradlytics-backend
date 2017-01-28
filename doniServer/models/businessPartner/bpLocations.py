from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .bpBasic import BpBasic


class BpLocation(models.Model):
    bp = models.ForeignKey(BpBasic,
                              null=False,
                              blank=False)
    address_id = models.AutoField(primary_key=True)
    address = models.TextField()
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None,  null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='bp_location_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='bp_location_updated_by')

    class Meta:
        db_table = 'bp_location'

    def json_obj(self):
        return {
            'id': self.address_id,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'created_by': self.created_by.username,
            'created_by_id': self.created_by.id,
            'created_at': self.created_at
        }

    def drop_down_obj(self):
        return {
            'id': self.address_id,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country
        }
