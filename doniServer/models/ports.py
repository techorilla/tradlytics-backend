from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone


class Port(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='port_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='port_updated_by')


    class Meta:
        db_table = 'port'
