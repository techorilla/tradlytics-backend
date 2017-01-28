from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from .trBasic import Transaction



class TrStatus(models.Model):
    ALL_STATUS = (
        ('Washout at Par', 'WASHOUT_AT_PAR'),
        ('Arrived', 'ARRIVED'),
        ('Shipped', 'SHIPPED'),
        ('Washout at X', 'WASHOUT_AT_X'),
        ('Completed', 'COMPLETED'),
        ('Not Shipped', 'NOT_SHIPPED')
    )
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    status = models.CharField(
        max_length=50,
        choices=ALL_STATUS,
        default='Not Shipped',
        blank=False
    )
    washout_at_par = models.FloatField(null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_status_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_status_updated_by')

    class Meta:
        db_table = 'tr_status'
