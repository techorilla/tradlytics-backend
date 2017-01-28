from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone


class BpType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='bp_type_created_by')
    updated_by = models.ForeignKey(User, default=None, null=True, blank=False, related_name='bp_type_updated_by')

    class Meta:
        db_table = 'bp_type'
        ordering = ('type',)
