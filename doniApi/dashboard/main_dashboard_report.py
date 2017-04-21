from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.businessPartner.bpBank import BpBank, BpBasic
from doniServer.models.manifest import ManifestItem
from doniServer.models.product import Products, PriceMetric
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
        user = request.user
        business = user.profile.business
        business_location = business.locations.get(is_primary=True)

        # USD Exchange Data

        usd_currency_data = self.get_currency_exchange_data(in_currency='USD', out_currency='PKR')

        return Response({'data': {
            'usdExchange': usd_currency_data
        }}, status=status.HTTP_200_OK)






