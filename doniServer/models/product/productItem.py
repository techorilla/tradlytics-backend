from .products import Products
from django.contrib.auth.models import User
from .productKeyword import ProductKeyword
from .productOrigin import ProductOrigin
from django.db import models
from .priceMarket import PriceMarket
from django.utils import timezone
from django.contrib import admin
from datetime import datetime as dt, timedelta



class ProductItem(models.Model):
    keywords = models.ManyToManyField(ProductKeyword, related_name='product_items')
    product_origin = models.ForeignKey(ProductOrigin, null=True, blank=False, related_name='origin_product_item')
    price_on_website = models.BooleanField(default=False)
    import_expense = models.FloatField(default=1.07)
    database_ids = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='prod_item_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='prod_item_updated_by')

    class Meta:
        ordering = ('id',)


    @classmethod
    def get_price_ticker(cls):
        day_before = dt.now() - timedelta(days=1)
        ticker_products = ProductItem.objects.filter(price_on_website=True).distinct()
        ticker_items = []
        for product_item in ticker_products:
            day_before_local_price = product_item.price_product_item.filter(
                price_time__startswith=day_before,
                price_market__origin='PK').order_by('-price_time')
            local_price = product_item.price_product_item.filter(
                price_time__startswith=dt.now().date(),
                price_market__origin='PK').order_by('-price_time')
            day_before_int_price = product_item.price_product_item.filter(
                price_time__startswith=day_before,
                price_market__origin='PK').order_by('-price_time')
            int_price = product_item.price_product_item.filter(
                price_time__startswith=dt.now().date(),
                price_market__origin='int').order_by('-price_time')
            local_price = None if not local_price.exists() else local_price.first()
            int_price = None if not int_price.exists() else int_price.first()
            item = (product_item, int_price, local_price, day_before_int_price, day_before_local_price)
            ticker_items.append(item)
        ticker_obj = []
        for (product_item, international, local, day_before_int_price, day_before_local_price) in ticker_items:
            item = dict()
            item['name'] = product_item.product_origin.product.name
            item['productCode'] = product_item.product_origin.product.product_code if \
                product_item.product_origin.product.product_code  else product_item.product_origin.product.name
            item['flagUrl'] = product_item.product_origin.country.flag
            item['id'] = product_item.id
            item['country'] = product_item.product_origin.country.code
            item['keywords'] = product_item.keyword_str
            item['localPrice'] = 'NA' if not local else '%s %.2f / %s'% (
                local.price_market.currency,
                local.current_price,
                local.price_metric.metric)
            try:
                item['localPriceChange'] = float(local.current_price - day_before_local_price.current_price) if day_before_local_price else 0.00
            except:
                item['localPriceChange'] = 0.00
            item['localPrice_pkr_pkg'] = 'NA' if not local else 'Rs %.2f / kg' % local.rs_per_kg

            try:
                item['localPrice_pkr_pkg_change'] = float(local.rs_per_kg - day_before_local_price.rs_per_kg) if day_before_local_price else 0.00
            except:
                item['localPrice_pkr_pkg_change'] = 0.00

            item['localPrice_usd_pmt'] = 'NA' if not local else 'US$ %.2f / MT' % local.usd_per_pmt
            item['localPrice_usd_pmt_change'] = float(local.usd_per_pmt - day_before_local_price.usd_per_pmt) if day_before_local_price else 0.00
            item['internationalPrice'] = 'NA' if not international else '%s %s/%s' % (
                international.price_market.currency,
                international.current_price,
                international.price_metric.metric)
            item['internationalPriceChange'] = float(international.current_price - day_before_int_price.current_price) if day_before_int_price else 0.00
            item['internationalPrice_pkr_pkg'] = 'NA' if not international else 'Rs %.2f / kg' % international.rs_per_kg
            try:
                item['internationalPrice_pkr_pkg_change'] = float(international.rs_per_kg - day_before_int_price.rs_per_kg) if day_before_int_price else 0.00
            except:
                item['internationalPrice_pkr_pkg_change'] = 0.00

            item['internationalPrice_usd_pmt'] = 'NA' if not international else 'US$ %.2f / MT' % international.usd_per_pmt

            try:
                item['internationalPrice_usd_pmt_change'] = float(international.usd_per_pmt - day_before_int_price.usd_per_pmt) if day_before_int_price else 0.00
            except:
                item['internationalPrice_usd_pmt_change'] = 0.00
            ticker_obj.append(item)
        return ticker_obj







    def get_dropdown(self):
        return {
            'id': self.id,
            'name': self.product_origin.product.name,
            'importExpense': self.import_expense,
            'origin': self.product_origin.country.name,
            'originFlag': self.product_origin.country.flag,
            'keywords': self.keyword_str
        }

    def get_price_website(self, market='INT'):
        if market == 'INT':
            last_two_prices = self.get_last_two_international_market_rate()
        else:
            last_two_prices = self.get_last_two_local_market_rate()
        if last_two_prices:
            last_price = last_two_prices[0]

            last_time = last_price.price_time
            l_price = float(last_price.get_market_current_price)
            try:
                second_last_price = last_two_prices[1]
                s_price = float(second_last_price.get_market_current_price)
                change = float(l_price - s_price)
                percentange_change = (change/s_price)*100
            except IndexError:
                change = 'NA'
                s_price = 'NA'
                percentange_change = 'NA'
            return {
                'id': self.id,
                'productCode': self.product_origin.product.product_code if self.product_origin.product.product_code else self.product_origin.product.name,
                'origin': self.product_origin.country.code,
                'originFlag': self.product_origin.country.flag,
                'name': self.product_origin.product.name,
                'keywords': self.keyword_str,
                'lastPrice': '%.2f' % l_price,
                'currency': last_price.price_market.currency,
                'secondLastPrice': s_price,
                'last_time': last_time,
                'priceChange': l_price,
                'change': change,
                'percentangeChange': percentange_change
            }
        else:
            return None


    @property
    def price_market_summary(self):
        international = self.get_last_two_international_market_rate()
        local = self.get_last_two_local_market_rate()
        if international:
            int_price_obj = international[0]
            int_price = float(int_price_obj.get_market_current_price)
            try:
                second_last_int_price = international[1]
                int_prev_price = float(second_last_int_price.get_market_current_price)
                int_change = float(int_price - int_prev_price)
                int_percentange_change = (int_change/int_prev_price)*100
            except IndexError:
                int_change = 'NA'
                int_prev_price = 'NA'
                int_percentange_change = 'NA'
        else:
            int_price_obj = None
            int_price = 'NA'
            int_change = 'NA'
            int_prev_price = 'NA'
            int_percentange_change = 'NA'

        if local:
            local_price_obj = local[0]
            local_price = float(local_price_obj.get_market_current_price)
            try:
                second_last_local_price = local[1]
                local_prev_price = float(second_last_local_price.get_market_current_price)
                local_change = float(local_price - local_prev_price)
                local_percentage_change = (local_change / local_prev_price) * 100
            except IndexError:
                local_change = 'NA'
                local_prev_price = 'NA'
                local_percentage_change = 'NA'
        else:
            local_price_obj = None
            local_price = 'NA'
            local_change = 'NA'
            local_prev_price = 'NA'
            local_percentage_change = 'NA'

        return {
            'intlastUpdated': int_price_obj.price_time if int_price_obj else 'NA',
            'locallastUpdated': local_price_obj.price_time if local_price_obj else 'NA',
            'productId': self.product_origin.product.id,
            'productItemId': self.id,
            'productOriginName': self.product_origin.country.name,
            'originFlag': self.product_origin.country.flag,
            'productName': self.product_origin.product.name,
            'keywords': self.keyword_str,
            'localMetric': local_price_obj.price_metric.metric if local_price_obj else 'NA',
            'internationalMetric': int_price_obj.price_metric.metric if int_price_obj else 'NA',
            'localCurrency': local_price_obj.price_market.currency if local_price_obj else 'NA',
            'internationalCurrency': int_price_obj.price_market.currency if int_price_obj else 'NA',
            'monthLocalChange': local_price_obj.get_monthly_change if local_price_obj else {
                'change': 'NA',
                'percentageChange': 'NA'
            },
            'weeklyLocal':  local_price_obj.get_weekly_high_low() if local_price_obj else {'high': 'NA', 'low': 'NA'},
            'weeklyInternational': int_price_obj.get_weekly_high_low() if int_price_obj else {'high': 'NA', 'low': 'NA'},
            'monthlyLocal': local_price_obj.get_monthly_high_low() if local_price_obj else {'high': 'NA', 'low': 'NA'},
            'monthlyInternational': int_price_obj.get_monthly_high_low() if int_price_obj else {'high': 'NA', 'low': 'NA'},
            'internationalPrice': round(int_price, 2) if int_price != 'NA' else int_price,
            'interationalPrevPrice': round(int_prev_price, 2) if int_prev_price !='NA' else int_prev_price,
            'internationalChange': round(int_change, 2) if int_change != 'NA' else int_change,
            'internationalPercentangeChange': round(int_percentange_change, 2) if int_percentange_change!='NA' else int_percentange_change,
            'localPrice': round(local_price, 2) if local_price != 'NA' else local_price,
            'localPrevPrice': round(local_prev_price, 2) if local_prev_price != 'NA' else local_prev_price,
            'localPercentangeChange': round(local_percentage_change, 2) if local_percentage_change != 'NA' else local_percentage_change,
            'localChange': round(local_change, 2) if local_change != 'NA' else local_change
        }


    def get_last_two_international_market_rate(self):
        international_market = PriceMarket.objects.get(origin='INT')
        product_price = self.price_product_item.all().filter(price_market=international_market).order_by('price_time')[:2]
        return product_price

    def get_last_two_local_market_rate(self):
        local_market = PriceMarket.objects.get(origin='PK', currency='PKR')
        product_price = self.price_product_item.all().filter(price_market=local_market).order_by('price_time')[:2]
        return product_price

    @property
    def keywords_ids(self):
        keywords = self.keywords.all()
        print keywords
        return [key.id for key in keywords]

    @property
    def keyword_str(self):
        keywords = self.keywords.all()
        keywords = [str(key.keyword) for key in keywords]
        return ', '.join(keywords)

    def get_obj(self):
        return {
            'id': self.id,
            'importExpense': self.import_expense,
            'productId': self.product_origin.product.id,
            'productName': self.product_origin.product.name,
            'databaseIds': self.database_ids,
            'priceOnWebsite': self.price_on_website,
            'origin': self.product_origin.country.code.upper(),
            'productOriginName': self.product_origin.country.name,
            'productOriginFlag': self.product_origin.country.flag,
            'keywords': self.keywords_ids,
            'keywordsString': self.keyword_str,
            'updatedBy': self.updated_by.username if self.updated_by else None,
            'updatedAt': self.updated_at,
            'createdBy': self.created_by.username,
            'createdAt': self.created_at
        }


class ProductItemAdmin(admin.ModelAdmin):
    model = Products
    list_display = ('product_origin','database_ids', 'keyword_str')


