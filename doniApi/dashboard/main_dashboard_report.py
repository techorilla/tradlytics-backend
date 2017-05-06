from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.businessPartner.bpBank import BpBank, BpBasic
from doniServer.models.manifest import ManifestItem
from django.db.models import Count
from django.db.models.aggregates import Max

from doniServer.models.product import Products, PriceMetric, ProductItemPrice
from datetime import datetime as dt, timedelta
import pycountry
from doniServer.models import CurrencyExchange
import pandas as pd


class MainDashboardAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get_currency_exchange_data(self, in_currency='USD', out_currency='PKR'):

        rates = CurrencyExchange.objects\
            .filter(currency_code_in=in_currency, currency_code_out=out_currency)\
            .order_by('-exchange_rate_on')\
            .values('currency_code_in', 'currency_code_out', 'exchange_rate', 'exchange_rate_on')[:7]
        todays_rate = rates[0].get('exchange_rate')
        day_before_rate = rates[1].get('exchange_rate')
        change = (float(todays_rate - day_before_rate)/day_before_rate)*100
        seven_days = [{
            'rate': rate.get('exchange_rate'),
            'date': rate.get('exchange_rate_on')
        } for rate in rates]
        seven_days.reverse()
        return {
            'lastUpdate': rates[0].get('exchange_rate_on'),
            'inputCurrency': in_currency,
            'outCurrency': out_currency,
            'sevenDays': seven_days,
            'currentValue': todays_rate,
            'change': change
        }

    def get(self, request, *args, **kwargs):
        today = dt.now()
        start_time = today - timedelta(hours=24)
        end_time = today
        user = request.user
        business = user.profile.business
        business_location = business.locations.get(is_primary=True)

        # USD Exchange Data
        usd_currency_data = self.get_currency_exchange_data(in_currency='USD', out_currency='PKR')

        # Get Price Updates Number
        price_update_count = ProductItemPrice.objects.filter(created_at__gte=start_time, created_at__lte=end_time).count()
        if price_update_count:
            price_update_last_time = ProductItemPrice.objects.filter(created_at__gte=start_time, created_at__lte=end_time)\
                .values('created_at').order_by('-created_at').first()
            price_update_last_time = price_update_last_time.get('created_at')
        else:
            price_update_last_time = 'NA'

        # Get Manifest Updates Number

        manifest_update_count = ManifestItem.objects.filter(created_at__gte=start_time, created_at__lte=end_time).count()
        manifest_top_three_contributors = []
        if manifest_update_count:

            top_three_contributors = ManifestItem.objects.filter(created_at__gte=start_time, created_at__lte=end_time)\
                .values('created_by__username')\
                .annotate(total=Count('created_by__username'))\
                .order_by('-total')

            for contrib in top_three_contributors:
                manifest_contributer = dict()
                manifest_contributer['username'] = contrib['created_by__username']
                manifest_contributer['updates'] = contrib['total']
                last_update = ManifestItem.objects.filter(created_by__username=manifest_contributer['username'])\
                    .order_by('-created_at').values('created_at').first()
                manifest_contributer['lastUpdate'] = last_update.get('created_at')
                manifest_top_three_contributors.append(manifest_contributer)


        return Response({'data': {
            'usdExchange': usd_currency_data,
            'priceUpdate':{
                'count': price_update_count,
                'lastUpdate': price_update_last_time
            },
            'manifestUpdate':{
                'count':manifest_update_count,
                'topThreeContributors': manifest_top_three_contributors
            }
        }}, status=status.HTTP_200_OK)






