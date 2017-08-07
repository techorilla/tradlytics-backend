from __future__ import unicode_literals

from django.db import models
from doniServer.models import Transaction
from doniInventory.models import Warehouse
from doniServer.models import BpBasic, ProductItem
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.



class LocalTrade(models.Model):
    date = models.DateField(null=False)
    buyer = models.ForeignKey(BpBasic, null=False, related_name='tr_local_buyer')
    seller = models.ForeignKey(BpBasic, null=False, related_name='tr_local_seller')
    product_item = models.ForeignKey(ProductItem, null=True)
    quantity_fcl = models.FloatField(default=0.00)
    quantity = models.FloatField(default=None)
    price = models.FloatField(default=None)
    file_id = models.CharField(max_length=100, null=False, unique=True, blank=False)
    international_file_id = models.ForeignKey(Transaction, null=True)
    contract_id = models.CharField(max_length=100, null=True)
    other_info = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_local_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_local_updated_by')

class LocalTradeChangeLog(models.Model):
    local_trade = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        null=True,
        related_name='change_log'
    )
    time = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    user = models.ForeignKey(User, null=False, blank=False, related_name='local_trade_changes_by')

    class Meta:
        db_table = 'local_change_log'

    def get_obj(self):
        return {
            'changeByUserName': self.user.username,
            'changeByUserId': self.user.id,
            'description': self.description,
            'changeTime': self.time
        }

    @classmethod
    def add_change_log(cls, user, description, local_trade):
        change_log = cls()
        change_log.user = user
        change_log.description = description
        change_log.local_trade = local_trade
        change_log.save()


class LocalTradeNotes(models.Model):
    localTrade = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    note_id = models.AutoField(primary_key=True)
    note = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='local_note_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='local_note_updated_by')

    def get_obj(self, base_url, user):
        return {
            'self': (self.created_by == user),
            'noteId': self.note_id,
            'isDeleteAble': (self.created_by == user) or user.is_superuser,
            'note': self.note,
            'createdAt': self.created_at,
            'createdBy': self.created_by.username,
            'createdByPic': self.created_by.profile.get_profile_pic(base_url),
            'updatedAt': self.updated_by
        }

    class Meta:
        db_table = 'local_notes'


class LocalTradeStatus(models.Model):
    localTrade = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='status'
    )
    delivery_due = models.BooleanField(default=True)
    delivery_due_date = models.DateField(null=True)
    delivery_done = models.BooleanField(default=False)
    delivery_done_date = models.DateField(null=True)
    delivery_reached = models.BooleanField(default=False)
    delivery_reached_date = models.DateField(null=True)
    funds_due = models.BooleanField(default=False)
    funds_due_date = models.DateField(null=True)
    completion_status = models.BooleanField(default=False)
    completion_status_date = models.DateField(default=True)


class PaymentTerm(models.Model):
    localTrade = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='payment_terms'
    )
    advance = models.BooleanField(default=False)
    on_delivery_reached = models.BooleanField(default=False)
    on_date = models.BooleanField(default=False)
    on_date_date = models.DateField(null=True)

    def save(self):
        if self.advance or self.on_delivery_reached:
            self.on_date_date = None
        super(PaymentTerm, self).save()

class DeliverySlip(models.Model):
    date = models.DateField(null=False)
    delivery_date = models.DateField(null=True)
    warehouse = models.ForeignKey(Warehouse, null=False)
    lot_no = models.CharField(max_length=10, null=False)
    localTrade = models.ForeignKey(
        LocalTrade,
        on_delete=models.CASCADE,
        related_name='delivery_slip'
    )
    notes = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='local_delivery_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='local_delivery_updated_by')

