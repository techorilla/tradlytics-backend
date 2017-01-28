from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone


class Origin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='origin_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='origin_updated_by')

    class Meta:
        db_table = 'origin'

    def __unicode__(self):
        return self.name

    @classmethod
    def get_origin_id(cls, name):
        origin = cls.get_origin_by_name(name=name)
        return origin.id

    @classmethod
    def get_origin_by_name(cls, name):
        return cls.objects.get(name=name)
