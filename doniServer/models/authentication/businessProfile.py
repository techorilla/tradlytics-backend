from django.db import models
from ..businessPartner.bpBasic import BpBasic

class BusinessAppProfile(models.Model):
    business = models.OneToOneField(BpBasic, related_name='app_profile')
    other_companies = models.ManyToManyField(BpBasic, related_name='business_other_companies')
    currency = models.CharField(max_length=20, null=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'business_profile'

    @property
    def all_associated_companies_id(self):
        associated_ids = list()
        associated_ids.append(self.business.bp_id)
        all_other = self.other_companies.all().values('bp_id')
        all_other_id = [id.get('bp_id') for id in all_other]
        return associated_ids+all_other_id


    def on_our_contract(self, business):
        return (self.business == business) or \
               (business.business_other_companies.filter(business__bp_id=self.business.bp_id).exists())



