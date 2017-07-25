from django.db import models
from django.contrib.auth.models import User
from .trBasic import Transaction
from .trChangeLog import TransactionChangeLog
from django.utils import timezone


class TrSellerInvoice(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='seller_invoice'
    )
    tr_seller_invoice_no=models.CharField(max_length=50)
    tr_seller_invoice_amount_usd=models.FloatField(default=0.00)

    class Meta:
        db_table = 'tr_seller_invoice'

    @classmethod
    def save_seller_invoice(cls, invoice_no, invoice_amount, transaction):
        update = True if hasattr(transaction, 'seller_invoice') else False
        seller_invoice = cls() if not update else transaction.seller_invoice

        if (update and (seller_invoice.tr_seller_invoice_no == invoice_no)
            and (seller_invoice.tr_seller_invoice_amount_usd == invoice_amount)):
            return

        else:
            seller_invoice.tr_seller_invoice_no = invoice_no
            seller_invoice.tr_seller_invoice_amount_usd = invoice_amount
            seller_invoice.transaction = transaction
            seller_invoice.save()


