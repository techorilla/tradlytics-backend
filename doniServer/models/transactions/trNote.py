from django.db import models
from django.contrib.auth.models import User
from .trBasic import Transaction
from django.utils import timezone


class TrNote(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    note_id = models.AutoField(primary_key=True)
    note = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_note_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_note_updated_by')

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
        db_table = 'tr_note'
