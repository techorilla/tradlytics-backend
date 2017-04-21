from django.db import models
from django.contrib.auth.models import User
from .trBasic import Transaction
from ..businessPartner import BpBasic
from django.utils import timezone


class SecondaryTransaction(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE
    )
    tr_sec_id = models.AutoField(primary_key=True)
    date = models.DateField(null=False)
    buyer = models.ForeignKey(BpBasic, null=True, related_name='tr_secondary_buyer')
    seller = models.ForeignKey(BpBasic, null=True, related_name='tr_secondary_seller')
    buyer_price = models.FloatField(default=0.00)
    seller_price = models.FloatField(default=0.00)
    other_info = models.TextField()
    quantity = models.FloatField(default=0.00)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_secondary_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_secondary_updated_by')


    class Meta:
        db_table = 'tr_secondary'
