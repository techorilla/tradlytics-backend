from django.db import models
from django.contrib.auth.models import User
from .trBasic import Transaction
from datetime import date
from django.utils import timezone


class TransactionChangeLog(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        null=True,
        related_name='change_log'
    )
    time = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    user = models.ForeignKey(User, null=False, blank=False, related_name='transaction_changes_by')

    class Meta:
        db_table = 'tr_change_log'


    def get_obj(self):
        return {
            'changeByUserName': self.user.username,
            'changeByUserId': self.user.id,
            'description': self.description,
            'changeTime': self.time
        }

    @classmethod
    def add_change_log(cls, user, description, transaction):
        change_log = cls()
        change_log.user = user
        change_log.description = description
        change_log.transaction = transaction
        change_log.save()

