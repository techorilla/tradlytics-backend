from django.db import models
from datetime import date
from django.contrib.auth.models import User
from .trBasic import Transaction
from ..businessPartner import BpBasic
from django.utils import timezone

class TrContract(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    doni_contract = models.BooleanField(default=False)
    own_contract = models.BooleanField(default=False)
    contractual_buyer = models.ForeignKey(BpBasic, null=True, related_name='contractual_buyer')

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_contract_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_contract_updated_by')

    class Meta:
        db_table = 'tr_contract'
