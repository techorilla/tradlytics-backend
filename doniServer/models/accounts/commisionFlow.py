from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
import time
from ..businessPartner.bpBasic import BpBasic
from ..transactions.trBasic import Transaction


COMMISSION_DESCRIPTION = {
    'INTERNATIONAL_TRADE_COMMISSION': 'International Trade Commission',
    'INTERNATIONAL_WASHOUT_COMMISSION': 'International Washout Commission'
}

class CommissionFlow(models.Model):
    business = models.ForeignKey(BpBasic, null=False, blank=False, related_name='commission_flow')
    international_trade = models.ForeignKey(Transaction, null=True, related_name='trade_commission_flow')
    flow_type_receivable = models.BooleanField(default=False)
    description = models.TextField()
    amount = models.FloatField(default=0.00)
    received = models.BooleanField(default=False)


    class Meta:
        db_table = 'commission_flow'

    @classmethod
    def save_international_transaction_commission(cls, trade, business, receivable=True):
        flow = cls()
        flow.international_trade = trade
        flow.flow_type_receivable = receivable
        flow.business = business
        flow.amount = trade.commission.quantity_commission
        flow.description = COMMISSION_DESCRIPTION['INTERNATIONAL_TRADE_COMMISSION']


    @classmethod
    def save_international_transaction_washout_commission(cls, trade):
        flow = cls()
        flow.international_trade = trade

        flow.save()









