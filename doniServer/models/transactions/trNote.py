from django.db import models
from django.contrib.auth.models import User
from .trBasic import Transaction
from django.utils import timezone


class TrNote(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE
    )
    note_id = models.AutoField(primary_key=True)
    note = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_note_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_note_updated_by')

    class Meta:
        db_table = 'tr_note'
