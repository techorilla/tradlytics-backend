from .products import Products
from django.contrib.auth.models import User
from .productKeyword import ProductKeyword
from .productOrigin import ProductOrigin
from django.db import models
from .priceMarket import PriceMarket
from django.utils import timezone
from django.contrib import admin
from datetime import datetime as dt, timedelta
from jsonfield import JSONField
from .productSpecification import ProductsSpecification
import json
import dateutil.parser
from django.db.models import Q



class ProductItem(models.Model):

    keywords = models.ManyToManyField(ProductKeyword, related_name='product_items')
    product_origin = models.ForeignKey(ProductOrigin, null=True, blank=False, related_name='origin_product_item')
    price_on_website = models.BooleanField(default=False)
    price_on_website_order = models.IntegerField(default=100, null=False)
    import_expense = models.FloatField(default=1.07)
    specification = JSONField(null=True)
    database_ids = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='prod_item_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='prod_item_updated_by')

    class Meta:
        ordering = ('id',)


    def __unicode__(self):
        return '%s:%s:%s'%(self.product_origin.product.name, self.product_origin.country, self.product_origin.product.category.name)

    @classmethod
    def get_product_with_database_id(cls, database_id):
        if ProductItem.objects.filter(database_ids=database_id).exists():
            return ProductItem.objects.get(database_ids=database_id)
        else:
            id_string = [str(database_id)+',',',' + str(database_id) + ',',','+str(database_id)]
            return ProductItem.objects.get(Q(database_ids__startswith=id_string[0]) | Q(database_ids__contains=id_string[1]) | Q(database_ids__startswith=id_string[2]))



    @classmethod
    def get_price_ticker(cls):
        price_date = dt.now()
        day_before = price_date - timedelta(days=1)
        ticker_products = ProductItem.objects.filter(price_on_website=True).order_by('price_on_website_order').order_by('price_on_website_order').distinct()
        last_update = ProductItem.objects\
                .filter(price_on_website=True).values('price_product_item__price_time').order_by('-price_product_item__price_time').first()
        last_update =  last_update.get('price_product_item__price_time')
        last_update =  dateutil.parser.parse(str(last_update).replace('"', ''))

        price_exists_for_today = False

        while not price_exists_for_today:
            price_exists_for_today = ProductItem.objects\
                .filter(price_product_item__price_time__startswith=price_date.date(), price_on_website=True).exists()
            if price_exists_for_today:
                day_before = price_date - timedelta(days=1)
                break
            price_date = price_date - timedelta(days=1)


        price_exists_for_day_before = False

        while not price_exists_for_day_before:
            price_exists_for_day_before = ProductItem.objects \
                .filter(price_product_item__price_time__startswith=day_before.date(), price_on_website=True).exists()
            if price_exists_for_day_before:
                break
            day_before = day_before - timedelta(days=1)

        ticker_items = []
        for product_item in ticker_products:
            day_before_local_price = product_item.price_product_item.filter(
                price_time__startswith=day_before.date(),
                price_market__origin='PK').order_by('-price_time')
            local_price = product_item.price_product_item.filter(
                price_time__startswith=price_date.date(),
                price_market__origin='PK').order_by('-price_time')
            day_before_int_price = product_item.price_product_item.filter(
                price_time__startswith=day_before.date(),
                price_market__origin='INT').order_by('-price_time')
            int_price = product_item.price_product_item.filter(
                price_time__startswith=price_date.date(),
                price_market__origin='int').order_by('-price_time')

            day_before_local_price = None if not day_before_local_price.exists() else day_before_local_price.first()
            local_price = None if not local_price.exists() else local_price.first()
            int_price = None if not int_price.exists() else int_price.first()
            day_before_int_price = None if not day_before_int_price.exists() else day_before_int_price.first()
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
                item['localPriceChange'] = round(item['localPriceChange'], 2)
            except:
                item['localPriceChange'] = 0.00
            item['localPrice_pkr_pkg'] = 'NA' if not local else 'Rs %s / kg' % round(local.rs_per_kg,2)
            try:
                item['localPrice_pkr_pkg_change'] = float(local.rs_per_kg - day_before_local_price.rs_per_kg) if day_before_local_price else 0.00
                item['localPrice_pkr_pkg_change'] = round(item['localPrice_pkr_pkg_change'], 2)
            except:
                item['localPrice_pkr_pkg_change'] = 0.00

            item['localPrice_usd_pmt'] = 'NA' if not local else 'US$ %s / MT' % round(local.usd_per_pmt, 2)


            try:
                item['localPrice_usd_pmt_change'] = float(local.usd_per_pmt - day_before_local_price.usd_per_pmt) if day_before_local_price else 0.00
                item['localPrice_usd_pmt_change'] = round(item['localPrice_usd_pmt_change'], 2)
            except:
                item['localPrice_usd_pmt_change'] = 0.00
            item['internationalPrice'] = 'NA' if not international else '%s %s/%s' % (
                international.price_market.currency,
                international.current_price,
                international.price_metric.metric)

            try:
                item['internationalPriceChange'] = float(international.current_price - day_before_int_price.current_price) if day_before_int_price else 0.00
            except AttributeError:
                item['internationalPriceChange'] = 0.00



            item['internationalPrice_pkr_pkg'] = 'NA' if not international else 'Rs %.2f / kg' % international.rs_per_kg
            try:
                item['internationalPrice_pkr_pkg_change'] = float(international.rs_per_kg - day_before_int_price.rs_per_kg) if day_before_int_price else 0.00
                item['internationalPrice_pkr_pkg_change'] = round(item['internationalPrice_pkr_pkg_change'], 2)
            except:
                item['internationalPrice_pkr_pkg_change'] = 0.00

            item['internationalPrice_usd_pmt'] = 'NA' if not international else 'US$ %.2f / MT' % international.usd_per_pmt

            try:
                item['internationalPrice_usd_pmt_change'] = float(international.usd_per_pmt - day_before_int_price.usd_per_pmt) if day_before_int_price else 0.00
                item['internationalPrice_usd_pmt_change'] = round(item['internationalPrice_usd_pmt_change'], 2)
            except:
                item['internationalPrice_usd_pmt_change'] = 0.00
            ticker_obj.append(item)
        return ticker_obj, last_update







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
        int_price, last_int_price  = self.get_last_two_prices_for_market('INT')
        local_price, last_local_price = self.get_last_two_prices_for_market('PK')

        if int_price:
            int_price_val = float(int_price.usd_per_pmt)
            try:
                second_last_int_price = last_int_price
                int_prev_price = float(second_last_int_price.usd_per_pmt)
                int_change = float(int_price_val - int_prev_price)
                int_percentange_change = (int_change/int_prev_price)*100
            except Exception, e:
                int_change = 'NA'
                int_prev_price = 'NA'
                int_percentange_change = 'NA'
            print int_price, int_prev_price
        else:
            int_price = None
            int_price_val = 'NA'
            int_change = 'NA'
            int_prev_price = 'NA'
            int_percentange_change = 'NA'

        if local_price:
            local_price_val = float(local_price.rs_per_kg)
            try:
                second_last_local_price = last_local_price
                local_prev_price = float(second_last_local_price.rs_per_kg)
                local_change = float(local_price_val - local_prev_price)
                local_percentage_change = (local_change / local_prev_price) * 100
            except Exception, e:
                local_change = 'NA'
                local_prev_price = 'NA'
                local_percentage_change = 'NA'
        else:
            local_price = None
            local_price_val = 'NA'
            local_change = 'NA'
            local_prev_price = 'NA'
            local_percentage_change = 'NA'

        return {
            'intLastUpdated': int_price.price_time + timedelta(hours=5) if int_price  else 'NA',
            'localLastUpdated': local_price.price_time  + timedelta(hours=5) if local_price else 'NA',
            'productId': self.product_origin.product.id,
            'productItemId': self.id,
            'productOriginName': self.product_origin.country.name,
            'originFlag': self.product_origin.country.flag,
            'productName': self.product_origin.product.name,
            'keywords': self.keyword_str,
            'localMetric': 'Kg' if local_price else 'NA',
            'internationalMetric': 'MT' if int_price else 'NA',
            'localCurrency': 'Rs' if local_price else 'NA',
            'internationalCurrency': 'US$' if int_price else 'NA',
            'monthLocalChange': local_price.get_monthly_change if local_price else {
                'change': 'NA',
                'percentageChange': 'NA'
            },
            'weeklyLocal':  local_price.get_weekly_high_low(metric='rs_per_kg') if local_price else {'high': 'NA', 'low': 'NA'},
            'weeklyInternational': int_price.get_weekly_high_low() if int_price else {'high': 'NA', 'low': 'NA'},
            'monthlyLocal': local_price.get_monthly_high_low(metric='rs_per_kg') if local_price else {'high': 'NA', 'low': 'NA'},
            'monthlyInternational': int_price.get_monthly_high_low() if int_price else {'high': 'NA', 'low': 'NA'},
            'internationalPrice': round(int_price_val, 2) if int_price_val != 'NA' else int_price_val,
            'interationalPrevPrice': round(int_prev_price, 2) if int_prev_price !='NA' else int_prev_price,
            'internationalChange': round(int_change, 2) if int_change != 'NA' else int_change,
            'internationalPercentangeChange': round(int_percentange_change, 2) if int_percentange_change!='NA' else int_percentange_change,
            'localPrice': round(local_price_val, 2) if local_price_val != 'NA' else local_price_val,
            'localPrevPrice': round(local_prev_price, 2) if local_prev_price != 'NA' else local_prev_price,
            'localPercentangeChange': round(local_percentage_change, 2) if local_percentage_change != 'NA' else local_percentage_change,
            'localChange': round(local_change, 2) if local_change != 'NA' else local_change
        }


    def get_last_two_prices_for_market(self, market='INT'):
        last_price = self.price_product_item.filter(price_market__origin=market).order_by('-price_time').first()
        day_before_last_price = None
        if last_price:
            last_price_date = last_price.price_time
            day_before_date = last_price_date - timedelta(days=1)
            day_before_last_price = self.price_product_item.filter(price_market__origin=market) \
                .filter(price_time__startswith=day_before_date.date()).order_by('-price_time').first()
        return last_price, day_before_last_price

    @property
    def keywords_ids(self):
        keywords = self.keywords.all()
        return [key.id for key in keywords]

    @property
    def keyword_str(self):
        keywords = self.keywords.all()
        keywords = [str(key.keyword) for key in keywords]
        return ', '.join(keywords)

    def get_specification(self):
        try:
            specs_config = self.product_origin.product.category.specification.specs
            item_specs = self.specification if self.specification else []
            for spec in specs_config:
                spec_item = [item for item in item_specs
                             if item.get(u'name','').lower() == spec.get(u'name', '').lower()]
                if spec_item:

                    spec_item = spec_item[0]
                    spec[u'value'] = spec_item.get(u'value') if spec_item else None
                else:
                    spec[u'value'] = None
            return specs_config
        except ProductsSpecification.DoesNotExist:
            return []

    @property
    def specs(self):
        try:
            specs_config = self.product_origin.product.category.specification.specs
            item_specs = self.specification if self.specification else []
            for spec in specs_config:
                spec_item = [item for item in item_specs
                             if item.get(u'name','').lower() == spec.get(u'name', '').lower()]
                if spec_item:

                    spec_item = spec_item[0]
                    spec[u'value'] = spec_item.get(u'value') if spec_item else None
                else:
                    spec[u'value'] = None
            return specs_config
        except ProductsSpecification.DoesNotExist:
            return []


    def get_obj(self):
        return {
            'id': self.id,
            'importExpense': self.import_expense,
            'productId': self.product_origin.product.id,
            'productName': self.product_origin.product.name,
            'databaseIds': self.database_ids,
            'specification': self.get_specification(),
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

    def get_description_obj(self, base_url):
        return {
            'image': self.product_origin.product.get_product_image(base_url),
            'name': self.product_origin.product.name,
            'id': self.id,
            'country': self.product_origin.country.name,
            'countryFlag': self.product_origin.country.flag
        }





class ProductItemAdmin(admin.ModelAdmin):
    model = Products
    list_display = ('product_origin','database_ids', 'keyword_str')


from django.db.models.signals import pre_save
def pre_save_post_receiver(sender, instance, *args, **kwargs):

    if not instance.import_expense:
        instance.import_expense = 1.06


pre_save.connect(pre_save_post_receiver, sender=ProductItem)



