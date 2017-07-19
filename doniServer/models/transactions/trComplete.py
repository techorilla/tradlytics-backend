from django.db import models
from django.contrib.auth.models import User
from .trBasic import Transaction
from .trChangeLog import TransactionChangeLog
from django.utils import timezone


class TrComplete(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='completion_status'
    )
    is_complete = models.BooleanField(default=False)
    completion_date = models.DateField(null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_complete_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_complete_updated_by')


    class Meta:
        db_table = 'tr_complete'


    def get_description_obj(self):
        return {
            'completionDate': self.completion_date,
            'isComplete': self.is_complete
        }

from django.db.models.signals import post_save
from notifications.signals import notify

def my_handler(sender, instance, created, **kwargs):
    user = instance.created_by if created else instance.updated_by
    transaction = instance.transaction
    peers = user.profile.get_notification_peers()
    if instance.is_complete:
        log = 'Changed transaction status to <span class="titled">COMPLETED</span>.'
        peer_notification = 'File %s set to completed by %s'%(transaction.file_id, user.username)
    else:
        log = 'Changed transaction status to <span class="titled">INCOMPLETE</span> from <span class="titled">COMPLETED</span>.'
        peer_notification = 'File %s set to incomplete by %s' % (transaction.file_id, user.username)

    TransactionChangeLog.add_change_log(user, log, transaction)
    notify.send(user, recipient=peers, verb=peer_notification, description='international_trade',
                state='dashboard.transactionView',
                state_id=transaction.file_id, user_image=user.profile.get_profile_pic())

post_save.connect(my_handler, sender=TrComplete)