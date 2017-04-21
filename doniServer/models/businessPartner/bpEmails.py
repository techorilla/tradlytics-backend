from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone
from .bpBasic import BpBasic


class BpEmail(models.Model):
    bp = models.ForeignKey(BpBasic,
                              null=False,
                              blank=False)
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True, null=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='bp_emails_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='bp_emails_updated_by')

    class Meta:
        db_table = 'bp_emails'
