from ..models import ProductItem, PriceSummary
from datetime import datetime as dt


class PriceSummaryRoutine(object):

    def __init__(self):
        return None

    ## This routine is expected to run everyday

    def run_routine(self):
        date = dt.now()
        product_items = ProductItem.objects.all()
        for product in product_items:
            summary = PriceSummary()
            summary.summary_on = date
            summary.product_item = product
            summary.summary = product.price_market_summary
            summary.save()


