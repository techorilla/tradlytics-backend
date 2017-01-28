from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .bpBasic import BpBasic


class BpBank(models.Model):
    bp = models.ForeignKey(BpBasic,
                              null=False,
                              blank=False)
    acc_id = models.AutoField(primary_key=True)
    branch_address = models.CharField(max_length=250, null=False, blank=False)
    bank_name = models.CharField(max_length=100, null=False)
    acc_title = models.CharField(max_length=150, null=False)
    acc_number = models.CharField(max_length=100, null=False)
    acc_country = models.CharField(max_length=250, null=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None,  null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='bp_bank_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='bp_bank_updated_by')

    class Meta:
        db_table = 'bp_bank'
