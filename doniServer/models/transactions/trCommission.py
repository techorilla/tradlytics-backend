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

    #Total Commission (Auto Calculate)
    expected_commission = models.FloatField(default=0.00)
    actual_commission = models.FloatField(default=0.00)

    #Quantity Shipped
    quantity_shipped = models.FloatField(default=0.00)

    #Commission Accounts (Auto Calculate)
    buyer_broker_commission_actual = models.FloatField(default=0.00)
    buyer_broker_commission_expected = models.FloatField(default=0.00)
    buyer_commission_expected = models.FloatField(default=0.00)
    seller_commission_expected = models.FloatField(default=0.00)
    buyer_commission_actual = models.FloatField(default=0.00)
    seller_commission_actual = models.FloatField(default=0.00)

    @classmethod
    def recalculate_all_commission(cls):
        all_commission = cls.objects.all()
        for commission in all_commission:
            commission.save()




    class Meta:
        db_table = 'tr_commission'

    @property
    def commission_into_price(self):
        if self.commission_type.name == 'Fixed':
            return float(self.commission)
        else:
            return float(self.commission) * 0.01 * float(self.transaction.price)


    @property
    def buyer_broker_commission_into_price(self):
        if self.buyer_broker_comm and self.buyer_broker_comm_type:
            if self.buyer_broker_comm_type.name == 'Fixed':
                return float(self.buyer_broker_comm)
            else:
                return float(self.buyer_broker_comm) * 0.01 * float(self.transaction.price)
        else:
            return 0.00

    @property
    def calculate_actual_commission(self):
        return self.calculate_commission(self.quantity_shipped)

    @property
    def calculate_expected_commission(self):
        return self.calculate_commission(self.transaction.quantity)

    @property
    def calculate_buyer_broker_expected_commission(self):
        return self.calculate_buyer_broker_commission(self.transaction.quantity)

    @property
    def calculate_buyer_broker_expected_commission(self):
        return self.calculate_buyer_broker_commission(self.quantity_shipped)

    @property
    def calculate_buyer_expected_commission(self):
        return self.calculate_buyer_commission(self.transaction.quantity)

    @property
    def calculate_buyer_actual_commission(self):
        return self.calculate_buyer_commission(self.quantity_shipped)


    @property
    def calculate_seller_expected_commission(self):
        return self.calculate_seller_commission(self.transaction.quantity)

    @property
    def calculate_seller_actual_commission(self):
        return self.calculate_seller_commission(self.quantity_shipped)

    def calculate_seller_commission(self, quantity):
        return self.commission_into_price * quantity

    def calculate_buyer_commission(self, quantity):
        discount = float(self.discount)
        difference = float(self.difference)
        return (difference - discount) * quantity


    def calculate_buyer_broker_commission(self, quantity):
        return self.buyer_broker_commission_into_price * quantity


    def calculate_commission(self, quantity):
        comm_into_price = self.commission_into_price
        broker_comm_into_price = self.buyer_broker_commission_into_price
        difference = self.difference
        discount = self.discount
        commission = comm_into_price - broker_comm_into_price + difference - discount
        return commission * quantity


    def save(self):
        if self.quantity_shipped != 0.00:
            self.actual_commission = self.calculate_actual_commission
            self.buyer_broker_commission_actual = self.calculate_buyer_actual_commission
            self.seller_commission_actual = self.calculate_seller_actual_commission
            self.buyer_commission_actual = self.calculate_buyer_actual_commission

        self.expected_commission = self.calculate_expected_commission
        self.buyer_broker_commission_expected = self.calculate_buyer_broker_expected_commission
        self.seller_commission_expected = self.calculate_seller_expected_commission
        self.buyer_broker_commission_expected = self.calculate_buyer_expected_commission
        super(TrCommission, self).save()


    def get_description_obj(self, base_url):
        return {
            'typeId': self.commission_type.id,
            'price': self.transaction.price,
            'quantity': self.transaction.quantity,
            'quantityShipped': self.quantity_shipped,
            'sellerBroker': None if not self.seller_broker else self.seller_broker.get_description_ob(base_url),
            'buyerBroker': None if not self.buyer_broker else self.buyer_broker.get_description_obj(base_url),
            'buyerBrokerCommissionType': None if not self.buyer_broker else self.buyer_broker_comm_type.name,
            'buyerBrokerCommission': None if not self.buyer_broker else self.buyer_broker_comm,
            'commission': self.commission,
            'commissionType': self.commission_type.name,
            'difference': self.difference,
            'discount': self.discount,
            'expectedCommission': 'NA' if not self.expected_commission else str(round(self.expected_commission,2)),
            'actualCommission': str(round(self.actual_commission,2)),
            'expectedCommissionFlow':{
                'buyer': 'NA' if not self.buyer_broker_commission_expected else str(round(self.buyer_commission_expected,2)),
                'seller': 'NA' if not self.seller_commission_expected else str(round(self.seller_commission_expected,2)),
                'buyerBroker': 'NA' if not self.buyer_broker_commission_expected else str(round(self.buyer_commission_expected,2))
            },
            'actualCommissionFlow':{
                'buyer': str(round(self.buyer_commission_actual, 2)),
                'seller': str(round(self.seller_commission_actual, 2)),
                'buyerBroker': str(round(self.buyer_broker_commission_actual, 2))
            }
        }
