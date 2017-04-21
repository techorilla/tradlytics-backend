from django.db import models
from django.contrib.auth.models import User
from .trBasic import Transaction
from ..businessPartner.bpBasic import BpBasic
from django.utils import timezone


class TrCommission(models.Model):
    COMMISSION_TYPE = (
        ('Fixed', 'Fixed'),
        ('Percentage', 'Percentage')
    )
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    broker_involved = models.BooleanField(default=False)
    has_seller_broker = models.BooleanField(default=False)
    seller_broker = models.ForeignKey(BpBasic, null=True, related_name='seller_broker')
    seller_broker_comm_type = models.CharField(
        max_length=50,
        choices=COMMISSION_TYPE,
        default='Fixed',
    )
    seller_broker_comm = models.FloatField(default=0.00)
    has_buyer_broker = models.BooleanField(default=False)
    buyer_broker = models.ForeignKey(BpBasic, null=True, related_name='buyer_broker')
    buyer_broker_comm_type = models.CharField(
        max_length=50,
        choices=COMMISSION_TYPE,
        null=True
    )
    buyer_broker_comm = models.FloatField(default=0.00)
    own_comm = models.FloatField(default=None)
    own_comm_type = models.CharField(
        max_length=50,
        choices=COMMISSION_TYPE,
        null=True
    )
    differance = models.FloatField(default=0.00)
    discount = models.FloatField(default=0.00)
    net_commission = models.FloatField(default=0.00)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_commission_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_commission_updated_by')

    class Meta:
        db_table = 'tr_commission'
