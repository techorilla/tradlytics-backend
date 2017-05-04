from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone


class Packaging(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='packaging_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='packaging_updated_by')

    class Meta:
        db_table = 'product_packaging'
        ordering = ['-name']

    def drop_down_obj(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def get_list_obj(self):
        return {
            'id': self.id,
            'name': self.name,
            'createdAt': self.created_at,
            'createdBy': self.created_by.username,
            'createdById': self.created_by.id,
            'updatedAt': self.updated_at,
            'updatedBy': self.updated_by.username if self.updated_by else None,
            'updatedById': self.updated_by.id if self.updated_by else None
        }

    def __unicode__(self):
        return self.name