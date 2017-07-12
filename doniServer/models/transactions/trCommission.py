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
    earned_commission = models.FloatField(default=0.00)
    quantity_commission = models.FloatField(default=0.00)

    class Meta:
        db_table = 'tr_commission'


    def get_description_obj(self, base_url):
        return {
            'typeId': self.commission_type.id,
            'price': self.transaction.price,
            'quantity': self.transaction.quantity,
            'sellerBroker': None if not self.seller_broker else self.seller_broker.get_description_object(base_url),
            'buyerBroker': None if not self.buyer_broker else self.buyer_broker.get_description_objects(base_url),
            'buyerBrokerCommissionType': None if not self.buyer_broker else self.buyer_broker_comm_type.name,
            'buyerBrokerCommission': None if not self.buyer_broker else self.buyer_broker_comm,
            'commission': self.commission,
            'commissionType': self.commission_type.name,
            'difference': self.difference,
            'discount': self.discount,
            'netCommission': str(round(self.net_commission,2)),
            'earnedCommission': str(round(self.earned_commission,2))
        }
