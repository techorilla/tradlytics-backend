from django.db import models
from ..businessPartner.bpBasic import BpBasic
from django.utils import timezone


class ContactUs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    subject = models.TextField(max_length=250)
    message = models.TextField(max_length=250)
    business = models.ForeignKey(BpBasic, default=BpBasic.get_admin_business().bp_id)
    received_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "%s : %s" % (self.name, self.subject)
