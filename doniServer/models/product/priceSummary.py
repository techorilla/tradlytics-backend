from jsonfield import JSONField
from django.contrib.auth.models import User
from .productItem import ProductItem
from django.db import models
from django.utils import timezone
import dateutil.parser


class PriceSummary(models.Model):
    summary_on = models.DateTimeField(default=timezone.now)
    product_item = models.ForeignKey(ProductItem, null=False, related_name='summary')
    summary = JSONField(null=False)


    @property
    def international_price_update_time(self):
        try:
            return dateutil.parser.parse(self.summary.get('intlastUpdated'))
        except ValueError:
            return 'NA'

    @property
    def local_price_update_time(self):
        try:
            return dateutil.parser.parse(self.summary.get('locallastUpdated'))
        except ValueError:
            return 'NA'

    class Meta:
        db_table = 'product_price_summary'
        ordering = ('-summary_on',)
