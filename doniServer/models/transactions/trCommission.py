from django.db import models
from django.contrib.auth.models import User
from .trBasic import Transaction
from ..dropDowns.commissionType import CommissionType
from ..businessPartner.bpBasic import BpBasic
from django.utils import timezone


class TrCommission(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='commission'
    )
    seller_broker = models.ForeignKey(BpBasic, null=True, related_name='seller_broker')
    buyer_broker = models.ForeignKey(BpBasic, null=True, related_name='buyer_broker')
    buyer_broker_comm_type = models.ForeignKey(CommissionType, null=True, related_name='buyer_broker_commission_type')
    buyer_broker_comm = models.FloatField(default=0.00)
    commission = models.FloatField(default=None)
    commission_type = models.ForeignKey(CommissionType, null=True, related_name='trade_commission_type')
    difference = models.FloatField(default=0.00)
    discount = models.FloatField(default=0.00)
    net_commission = models.FloatField(default=0.00)

    class Meta:
        db_table = 'tr_commission'
