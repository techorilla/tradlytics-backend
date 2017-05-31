from django.db import models
from django.contrib.auth.models import User
from .trBasic import Transaction
from django.utils import timezone


class TrFiles(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE
    )
    file_id = models.AutoField(primary_key=True)
    file = models.BinaryField()
    extension = models.CharField(max_length=10, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_file_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_file_updated_by')

    class Meta:
        db_table = 'tr_files'
