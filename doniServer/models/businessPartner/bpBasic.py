from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone
from .bpTypes import BpType


class BpBasic(models.Model):
    bp_id = models.AutoField(primary_key=True)
    bp_name = models.CharField(max_length=255, blank=False, unique=True)
    bp_website = models.CharField(max_length=255, null=False, blank=False)
    bp_credibility_index = models.IntegerField(default=1)
    bp_country = models.CharField(max_length=250, null=True)
    bp_address = models.TextField(null=True, blank=True)
    bp_types = models.ManyToManyField(BpType)
    bp_on_contract = models.BooleanField(default=False)
    bp_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='bp_basic_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='bp_basic_updated_by')

    class Meta:
        db_table = 'bp_basic'

    @classmethod
    def get_admin_business(cls):
        return cls.objects.get(bp_admin=True)

    @classmethod
    def get_business_using_website(cls, url):
        return cls.objects.get(bp_website__contains=url)


