from django.db import models
from ..businessPartner.bpBasic import BpBasic

class BusinessAppProfile(models.Model):
    business = models.OneToOneField(BpBasic, related_name='app_profile')
    currency = models.CharField(max_length=20, null=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'business_profile'