from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone


class ProductKeyword(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=100, blank=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='keyword_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='keyword_updated_by')

    class Meta:
        db_table = 'product_keywords'
        ordering = ('keyword',)
