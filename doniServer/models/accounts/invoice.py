from django.contrib.auth.models import User
from django.db import models
from doniServer.models import Transaction
from django.utils import timezone
from django.conf import settings
import time
from jsonfield import JSONField
from .expenseType import ExpenseType
from datetime import datetime as dt

from ..authentication import BusinessAppProfile

from doniServer.models import CurrencyExchange

class IntTradeInvoice(models.Model):
    invoice_date = models.DateField(default=None, null=False)
    invoice_no = models.IntegerField(null=False)
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.PROTECT,
        null=True,
        related_name='invoices'
    )


    invoice_obj = JSONField(null=False)

    invoice_amount = models.FloatField(default=0.00, null=False)
    weight_in_kg = models.FloatField(null=False, default=0.00)
    rate_per_kg = models.FloatField(null=False, default=0.00)
    currency = models.CharField(max_length=20, null=False, default='PKR')

    note = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='invoice_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='invoice_updated_by')

    @classmethod
    def get_new_invoice_no(cls):
        if cls.objects.exists():
            invoice_no = cls.objects.all().order_by('-invoice_no').first().invoice_no
            return invoice_no
        else:
            return 1

    def save(self):
        business = self.created_by.profile.business
        currency = business.app_profile.currency
        self.currency = currency
        super(IntTradeInvoice, self).save()


    def get_complete_obj(self):

        return {
            'invoiceAmount': self.invoice_amount,
            'id': self.id,
            'price': self.transaction.price,
            'quantity': self.transaction.quantity,
            'fileNo': self.transaction.file_id,
            'contractNo': self.transaction.contract_id,
            'blNo': self.transaction.shipment.bl_no,
            'invoiceTo': self.transaction.contractual_buyer.get_description_obj(base_url),
            'productItem': self.transaction.product_item.get_description_obj(base_url),
            'date': dt.now().date(),
            'invoiceNo': self.invoice_no,
            'invoiceObj': self.invoice_obj,
            'note': self.note,
            'currency': self.currency
        }



    @classmethod
    def get_default_invoice_obj(cls, base_url, trade):
        trade_commission = trade.commission
        commission = trade_commission.actual_commission if trade_commission.actual_commission else trade_commission.expected_commission
        difference = trade_commission.difference
        discount = trade_commission.discount
        price = trade.price
        quantity = trade.commission.quantity_shipped if trade.commission.quantity_shipped else trade.quantity

        net_price = float(price)+float(difference)-float(discount)
        quantity_into_price = net_price * quantity
        business = trade.created_by.profile.business
        currency = business.app_profile.currency
        date, dollar_rate = CurrencyExchange.get_last_rate(currency)
        return {
            'invoiceAmount': 0.00,
            'currency': currency,
            'currencyRate': dollar_rate,
            'price': str(round(net_price,2)),
            'quantity': quantity,
            'fileNo': trade.file_id,
            'contractNo': trade.contract_id,
            'blNo': trade.shipment.bl_no,
            'invoiceTo': trade.buyer.get_description_obj(base_url),
            'productItem': trade.product_item.get_description_obj(base_url),
            'date': date,
            'invoiceNo': cls.get_new_invoice_no(),
            'invoiceItems': cls.get_default_invoice_expense_obj(trade.price, quantity_into_price, dollar_rate, commission=commission, currency=currency),
            'note': 'Invoice Sending By Courier'

        }

    @classmethod
    def get_default_invoice_expense_obj(cls, price, quantity_into_price, dollar_rate, commission='', currency='PKR', ):
        default_expenses = ExpenseType.objects.filter(default=True).order_by('default_order')
        default_expenses = [expense.get_default_expense_item_obj(price, quantity_into_price, dollar_rate, commission, currency) for expense in default_expenses]
        return default_expenses


























