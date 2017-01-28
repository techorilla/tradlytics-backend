from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ProductsSpecification(models.Model):
    id = models.AutoField(primary_key=True)

    moisture = models.FloatField(default=None, null=True)
    purity = models.FloatField(default=None, null=True)
    weaveled = models.FloatField(default=None, null=True)
    splits = models.FloatField(default=None, null=True)
    damaged = models.FloatField(default=None, null=True)
    foreignMatter = models.FloatField(default=None, null=True)
    greenDamaged = models.FloatField(default=None, null=True)
    otherColor = models.FloatField(default=None, null=True)
    wrinkled = models.FloatField(default=None, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='specs_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='specs_updated_by')

    class Meta:
        db_table = 'product_specs'

    def __unicode__(self):
        return self.name
