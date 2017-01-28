from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .bpBasic import BpBasic


class BpContactNumber(models.Model):
    bp = models.ForeignKey(BpBasic,
                              null=False,
                              blank=False)

    id = models.AutoField(primary_key=True)
    contact_number = models.CharField(max_length=254, null=False)
    type = models.CharField(max_length=50)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='bp_contact_number_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='bp_contact_number_updated_by')

    class Meta:
        db_table = 'bp_contact_number'
