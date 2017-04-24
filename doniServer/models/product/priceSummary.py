from jsonfield import JSONField
from django.contrib.auth.models import User
from .productItem import ProductItem
from django.db import models
from django.utils import timezone
import dateutil.parser
from datetime import datetime as dt


class PriceSummary(models.Model):
    summary_on = models.DateTimeField(default=timezone.now)
    product_item = models.ForeignKey(ProductItem, null=False, related_name='summary')
    summary = JSONField(null=False)


    @classmethod
    def get_price_summary_for_product(cls, product_item):
        new_summary = cls()
        new_summary.summary = product_item.price_market_summary
        new_summary.summary_on = dt.now()
        new_summary.product_item = product_item
        new_summary.save()

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
