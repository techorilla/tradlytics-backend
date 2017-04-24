from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PriceMetric(models.Model):
    metric = models.CharField(max_length=250, unique=True)
    kgs = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='price_metric_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='price_metric_updated_by')

    class Meta:
        db_table = 'price_metric'

    def __unicode__(self):
        return self.metric

    def get_drop_down(self):
        return {
            'id': self.metric,
            'name': self.metric
        }


from django.contrib import admin


class PriceMetricAdmin(admin.ModelAdmin):
    model = PriceMetric

