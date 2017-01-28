from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone
from .bpBasic import BpBasic


class BpContact(models.Model):
    bp = models.ForeignKey(BpBasic,
                              null=False,
                              blank=False)
    id = models.AutoField(primary_key=True)
    is_primary = models.BooleanField(default=False)
    full_name = models.CharField(max_length=100, null=False, blank=False)
    designation = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=254, null=True)
    primary_number = models.CharField(max_length=100, null=True)
    secondary_number = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='bp_contact_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='bp_contact_updated_by')

    class Meta:
        db_table = 'bp_contact'
