from django.db import models
from django.contrib.auth.models import User
from .trBasic import Transaction
from .trChangeLog import TransactionChangeLog
from django.utils import timezone

class TradeDispute(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='dispute'
    )
    dispute_date = models.DateField(null=False)
    quality_complain = models.BooleanField(default=False)
    weight_shortage = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    other_complain = models.BooleanField(default=False)
    dispute_resolved = models.BooleanField(default=False)
    dispute_resolved_date = models.DateField(null=True)
    details = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_dispute_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_dispute_updated_by')

    def get_description_obj(self):
        return {
            'isDisputed': True,
            'qualityComplain': self.quality_complain,
            'weightShortage': self.weight_shortage,
            'other': self.other,
            'disputeResolved': self.dispute_resolved,
            'disputeResolvedDate': self.dispute_resolved_date,
            'details': self.details,
            'disputeDate': self.dispute_date
        }

    class Meta:
        db_table = 'tr_dispute'



