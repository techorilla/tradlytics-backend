from django.contrib.auth.models import User
from django.db import models
from .productItem import ProductItem
from .priceMarket import PriceMarket
from .priceMetric import PriceMetric
from django.utils import timezone
from django.contrib import admin
from jsonfield import JSONField
from dateutil.relativedelta import relativedelta
import dateutil.parser
import numpy as np
import pytz
from django.contrib.auth.models import *
from django.conf import settings
from doniServer.models.exchangeRate import CurrencyExchange
from django.db.models.signals import pre_save
from django.db.models import Max


def fix_all_product_item():
    all_prices = ProductItemPrice.objects.all()
    for price in all_prices:
        exchange_rate = CurrencyExchange.objects.filter(exchange_rate_on__startswith=price.price_time.date())\
            .order_by('-exchange_rate_on').first()
        if not exchange_rate:
            exchange_rate = CurrencyExchange.objects.filter(exchange_rate_on__lte=price.price_time)\
            .order_by('-exchange_rate_on').first()
        price.current_price = price.get_market_current_price
        price.rs_per_kg = price.convert_rs_per_kg(exchange_rate.exchange_rate)
        price.usd_per_pmt = price.convert_usd_per_pmt(exchange_rate.exchange_rate)
        price.save()




class ProductItemPrice(models.Model):
    id = models.AutoField(primary_key=True)
    product_item = models.ForeignKey(ProductItem, null=False, related_name='price_product_item')
    price_market = models.ForeignKey(PriceMarket, null=False, related_name='price_market')
    price_metric = models.ForeignKey(PriceMetric, null=True, related_name='metric_prices')
    price_time = models.DateTimeField(default=timezone.now, db_index=True)
    price_items = JSONField(null=False)
    rs_per_kg = models.FloatField(null=True)
    usd_per_pmt = models.FloatField(null=True)
    current_price = models.FloatField(null=True)
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='prod_item_price_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='prod_item_price_updated_by')

    class Meta:
        db_table = 'product_item_price'
        ordering = ('-price_time',)


    def convert_rs_per_kg(self, exchange_rate):
        current_price = self.get_market_current_price
        metric = self.price_metric
        kgs = metric.kgs
        price_pkg = float(current_price)/kgs
        import_expense = self.product_item.import_expense
        currency = self.price_market.currency
        if currency == 'PKR':
            return float(price_pkg)
        elif currency == 'USD':
             return float(price_pkg * exchange_rate * import_expense)


    def convert_usd_per_pmt(self, exchange_rate):
        current_price = self.get_market_current_price
        metric = self.price_metric
        kgs = metric.kgs
        price_pkg = float(current_price)/kgs
        price_pmt = 1000*price_pkg
        import_expense = self.product_item.import_expense
        currency = self.price_market.currency
        if currency == 'USD':
            return float(price_pmt)
        elif currency == 'PKR':
            return float(float(price_pmt)/float(exchange_rate*import_expense))

    def get_weekly_high_low(self,  metric='usd_per_pmt'):

        ids_to_exclude = []
        found = False
        while found is False:
            week_prices = ProductItemPrice.objects \
                .filter(price_time__gte=self.month_before_date_time(months=1)) \
                .filter(price_time__lte=self.price_time) \
                .filter(price_market=self.price_market) \
                .filter(product_item=self.product_item) \
                .exclude(id__in=ids_to_exclude) \
                .order_by('-' + metric)

            week_prices_high = week_prices.first()
            week_prices_low = week_prices.last()

            found = True

        return {
            'high': round(getattr(week_prices_high, metric), 2),
            'low': round(getattr(week_prices_low, metric), 2)
        }

    def get_monthly_high_low(self, metric='usd_per_pmt'):
        ids_to_exclude=[]
        found = False
        while found is False:
            monthly_prices = ProductItemPrice.objects \
                .filter(price_time__gte=self.month_before_date_time(months=1)) \
                .filter(price_time__lte=self.price_time) \
                .filter(price_market=self.price_market) \
                .filter(product_item=self.product_item) \
                .exclude(id__in=ids_to_exclude) \
                .order_by('-'+metric)

            monthly_prices_high = monthly_prices.first()
            monthly_prices_low = monthly_prices.last()

            found = True

        return {
            'high': round(getattr(monthly_prices_high, metric), 2),
            'low': round(getattr(monthly_prices_low, metric), 2)
        }

    def month_before_date_time(self, months):
        price_time = self.price_time
        return price_time - relativedelta(months=months)

    def week_before_date_time(self, weeks):
        price_time = self.price_time
        days = 7 * weeks
        return price_time - relativedelta(days=days)

    @property
    def get_monthly_change(self):
        try:
            one_month_before = self.month_before_date_time(months=1)
            one_month_before_price = ProductItemPrice.objects.filter(price_time__lte=one_month_before) \
                                         .filter(price_market=self.price_market).filter(product_item=self.product_item)[:1]
            change = float(self.get_market_current_price) - float(one_month_before_price.get_market_current_price)
            percentage_change = float(change) / float(one_month_before_price.get_market_current_price)
            return {
                'change': change,
                'percentageChange': percentage_change
            }
        except Exception, e:
            return {
                'change': 'NA',
                'percentageChange': 'NA'
            }

    @property
    def get_weekly_change(self):
        one_week_before = self.week_before_date_time(weeks=1)
        try:
            one_week_before_price = ProductItemPrice.objects.filter(price_time__lte=one_week_before) \
                                        .filter(price_market=self.price_market).filter(product_item=self.product_item)[:1]
            change = float(self.get_market_current_price) - float(one_week_before_price.get_market_current_price)
            percentage_change = float(change) / float(one_week_before_price.get_market_current_price)
            return {
                'change': change,
                'percentageChange': percentage_change
            }
        except:
            return {
                'change': 'NA',
                'percentageChange': 'NA'
            }

    @property
    def get_market_current_price(self):
        price_items = self.price_items
        price = [item.get('priceValue') for item in price_items if item.get('currentValue')]
        price = price[0]
        return price




    @property
    def get_shipment_period_current_value(self):
        price_items = self.price_items
        price_shipment = [{
                              'price': item.get('priceValue'),
                              'shipmentMonths': item.get('shipmentMonths')
                           } for item in price_items if item.get('currentValue')]
        price_shipment = price_shipment[0]
        ship_months = price_shipment.get('shipmentMonths')
        try:
            start_ship = dateutil.parser.parse(ship_months[0])
            try:
                start_ship = (start_ship.astimezone(pytz.utc))
            except Exception, e:
                start_ship = pytz.utc.localize(start_ship)
                start_ship = start_ship.replace(tzinfo=pytz.UTC)
            days = (self.price_time-start_ship).days
        except Exception, e:
            days = np.nan

        price_shipment['price_time'] = self.price_time
        price_shipment['days'] = days if days >= 30 else 30
        price_shipment['market'] = str(self.price_market.country_name)
        price_shipment['market_currency'] = self.price_market.currency
        return price_shipment

    @classmethod
    def get_all_prices(cls, start_time, end_time):
        price_items = cls.objects.filter(price_time__gte=start_time, price_time__lte=end_time)
        price_items = [item.get_obj() for item in price_items]
        return price_items

    def get_obj(self):
        price_item = {
            'id': self.id,
            'showDetails': False,
            'product': self.product_item.product_origin.product.name,
            'productId': self.product_item.product_origin.product.id,
            'priceMarketId': self.price_market.id,
            'productName': self.product_item.product_origin.product.name,
            'productItemId': self.product_item.id,
            'priceItems': self.price_items,
            'priceMetric': self.price_metric.metric if self.price_metric else None,
            'priceMetricId': self.price_metric.metric if self.price_metric else None,
            'priceTime': self.price_time,
            'comments': self.comments,
            'keywords': self.product_item.keyword_str,
            'productOriginName': self.product_item.product_origin.country.name,
            'productOriginFlag': self.product_item.product_origin.country.flag,
            'marketCurrency': self.price_market.currency,
            'marketCountry': self.price_market.country_name,
            'currentPrice': self.get_market_current_price,
            'updatedBy': self.updated_by.username if self.updated_by else None,
            'updatedAt': self.updated_at,
            'createdBy': self.created_by.username if self.created_by else None,
            'createdAt': self.created_at
        }
        return price_item



def pre_save_product_item_price_receiver(sender, instance, *args, **kwargs):
    exchange_rate = CurrencyExchange.objects.filter(exchange_rate_on__lte=instance.price_time).order_by('-exchange_rate_on').first()
    instance.current_price = instance.get_market_current_price
    instance.rs_per_kg = instance.convert_rs_per_kg(exchange_rate.exchange_rate)
    instance.usd_per_pmt = instance.convert_usd_per_pmt(exchange_rate.exchange_rate)


pre_save.connect(pre_save_product_item_price_receiver, sender=ProductItemPrice)
