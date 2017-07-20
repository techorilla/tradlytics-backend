from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from .trBasic import Transaction
from .trChangeLog import TransactionChangeLog



class TrWashout(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        null=True,
        related_name='washout'
    )
    initial_commission_payable = models.BooleanField(default=True)
    washout_date = models.DateField(null=True)
    washout_due_date = models.DateField(null=True)
    is_washout = models.BooleanField(default=False)

    buyer_washout_price = models.FloatField(default=0.00)
    seller_washout_price = models.FloatField(default=0.00)
    broker_difference = models.FloatField(default=0.00)
    total_difference = models.FloatField(default=0.00)
    washout_commission = models.FloatField(default=0.00)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_washout_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_washout_updated_by')


    class Meta:
        db_table = 'tr_washout'

    ##:TODO Trigger for T accounts on




    def get_description_obj(self):
        return {
            'isWashout': self.is_washout,
            'initialCommissionPayable': self.initial_commission_payable,
            'washoutDate': self.washout_date,
            'washoutDueDate': self.washout_due_date,
            'buyerWashoutPrice': str(round(self.buyer_washout_price,2)),
            'sellerWashoutPrice': str(round(self.seller_washout_price,2)),
            'brokerDifference': str(round(self.broker_difference,2)),
            'totalDifference': str(round(self.total_difference,2)),
            'washOutCommission': str(round(self.washout_commission,2)),

        }

    @property
    def cash_flow_buyer(self):
        cash = self.total_difference - washOutCommission
        return cash, (cash>0)


    @property
    def cash_flow_seller(self):
        return self.total_difference , self.total_difference<0







from django.db.models.signals import pre_save, post_save, post_delete
from notifications.signals import notify

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    #saving washout Total Difference
    price = float(instance.transaction.price)
    quantity = float(instance.transaction.quantity)
    seller_price = float(instance.seller_washout_price)
    broker_difference = float(instance.broker_difference)
    price_difference = seller_price - price
    instance.total_difference = price_difference * quantity
    instance.washout_commission = broker_difference * quantity

def post_save_receiver(sender, instance, created, *args, **kwargs):
    user = instance.created_by if created else instance.updated_by
    peers = user.profile.get_notification_peers()

    if instance.is_washout:
        if created:
            log = '<span class="titled">Activated Washout Transaction Status!</span>'
            notification_msg = '<strong> File Id  %s</strong> washout status activated.' % instance.transaction.file_id
        else:
            log = '<span class="titled">Changed Transaction Washout Details!</span>'
            notification_msg = '<strong> File Id  %s</strong> washout details changed.' % instance.transaction.file_id
    else:
        notification_msg = '<strong> File Id  %s</strong> washout status deactivated changed.' % instance.transaction.file_id
        log='<span class="titled">Deactivated Transaction Washout Status!</span>'

    notify.send(user, recipient=peers, verb=notification_msg, description='international_trade',
                state='dashboard.transactionView', state_params={'id': instance.transaction.file_id},
                user_image=user.profile.get_profile_pic())

    TransactionChangeLog.add_change_log(user, log, instance.transaction)




pre_save.connect(pre_save_post_receiver, sender=TrWashout)
post_save.connect(post_save_receiver, sender=TrWashout)