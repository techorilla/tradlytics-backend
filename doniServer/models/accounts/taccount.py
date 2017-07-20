from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
import time
from .invoice import IntTradeInvoice
from ..businessPartner.bpBasic import BpBasic
from ..transactions.trBasic import Transaction
from datetime import datetime as dt


COMMISSION_DESCRIPTION = {
    'INTERNATIONAL_TRADE_COMMISSION': {'description': 'International Trade Commission', 'code': 1},
    'INTERNATIONAL_WASHOUT_COMMISSION': {'description': 'International Washout Commission', 'code': 2},
    'INTERNATIONAL_TRADE_ON_CONTRACT_INVOICE': {'description': 'International Trade On Our Contract Invoice', 'code': 3}
}

class TAccount(models.Model):
    due_date = models.DateField(null=False)
    business = models.ForeignKey(BpBasic, null=False, blank=False, related_name='t_account')
    international_trade = models.ForeignKey(Transaction, null=True, related_name='trade_commission_flow')
    int_invoice = models.ForeignKey(IntTradeInvoice, null=True, unique=True, related_name='invoice_t_accounts')
    debit = models.BooleanField(default=False)
    credit = models.BooleanField(default=False)
    description = models.TextField()
    code = models.IntegerField(null=False)
    amount = models.FloatField(default=0.00)

    is_due = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    business_account = models.ForeignKey(BpBasic, null=False, blank=False, related_name='business_account')



    class Meta:
        db_table = 't_accounts'

    def save(self):
        today = dt.now().date()
        if self.due_date.date() <= today:
            self.is_due = True
        super(TAccount, self).save()

    @classmethod
    def international_invoice_to_taccount(cls, new, invoice, business_account):
        if new:
            account = cls()
        else:
            account = cls.objects.get(int_invoice=invoice)

        account.business = invoice.invoice_to
        account.international_trade = invoice.transaction
        account.debit = True
        account.credit = False
        account.amount = invoice.invoice_amount
        account.int_invoice_no = invoice
        account.due_date = invoice.invoice_date
        account.description = COMMISSION_DESCRIPTION['INTERNATIONAL_TRADE_ON_CONTRACT_INVOICE']['description']
        account.code = COMMISSION_DESCRIPTION['INTERNATIONAL_TRADE_ON_CONTRACT_INVOICE']['code']
        account.business_account = business_account
        account.save()





from django.db.models.signals import post_save, post_delete
from notifications.signals import notify


def post_delete_handler(sender, instance, **kwargs):
    instance.invoice_t_accounts.all().delete()

def post_save_handler(sender, instance, created, **kwargs):

    if created or not instance.updated_by:
        user = instance.created_by
        peers = user.profile.get_notification_peers()
        peer_notification = 'New Invoice %s for File Id <strong>%s</strong> created by %s'
        peer_notification = peer_notification%(instance.invoice_no, instance.transaction.file_id, instance.created_by.username)
        notify.send(user, recipient=peers, verb=peer_notification, description='international_trade_invoice', state='dashboard.accounts.invoiceForm',
                    state_params={'invoiceId': instance.invoice_no, 'fileId': instance.transaction.file_id}, user_image=user.profile.get_profile_pic())


    else:
        user = instance.updated_by
        peers = user.profile.get_notification_peers()
        peer_notification = 'New Invoice %s for File Id <strong>%s</strong> created by %s'
        peer_notification = peer_notification % (instance.invoice_no, instance.transaction.file_id, instance.created_by.username)
        notify.send(user, recipient=peers, verb=peer_notification, description='international_trade_invoice', state='dashboard.accounts.invoiceForm',
                    state_params={'invoiceId':instance.invoice_no , 'fileId': instance.transaction.file_id}, user_image=user.profile.get_profile_pic())

    TAccount.international_invoice_to_taccount(created, instance, user.profile.business)

post_save.connect(post_save_handler, sender=IntTradeInvoice)
post_delete.connect(post_delete_handler, sender=IntTradeInvoice)







