from django.db import models
from django.contrib.auth.models import User
from .trBasic import Transaction
from django.utils import timezone
from doniServer.fields import VarBinaryField


class TrFiles(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='files'
    )
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=400, null=True)
    file = VarBinaryField()
    extension = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_file_created_by')

    class Meta:
        db_table = 'tr_files'
