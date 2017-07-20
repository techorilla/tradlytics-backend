from django.db import models
from ..businessPartner.bpBasic import BpBasic

class BusinessAppProfile(models.Model):
    business = models.OneToOneField(BpBasic, related_name='app_profile')
    other_companies = models.ManyToManyField(BpBasic, related_name='business_other_companies')
    currency = models.CharField(max_length=20, null=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'business_profile'


    def on_our_contract(self, business):
        return (self.business == business) or \
               (business.business_other_companies.filter(business__bp_id=self.business.bp_id).exists())



