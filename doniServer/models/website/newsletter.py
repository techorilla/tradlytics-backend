from django.db import models
from ..businessPartner.bpBasic import BpBasic
from django.utils import timezone


class NewsLetter(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=250)
    is_subscribed = models.BooleanField(default=True)
    business = models.ForeignKey(BpBasic, default=BpBasic.get_admin_business().bp_id)
    received_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "%s : %s" % (self.name, self.subject)

    def unsubscribe(self):
        self.is_subscribed = False
        self.save()
