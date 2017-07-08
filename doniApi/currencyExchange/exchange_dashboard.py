from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models.exchangeRate import CurrencyExchange
from datetime import datetime as dt
import pandas as pd
import dateutil.parser


class CurrencyExchangeDashboardAPI(GenericAPIView):

    def post(self, request, *args, **kwargs):
        print request.data
        start_date = request.data.get(u'startDate')
        end_date = request.data.get(u'endDate')
        currency_in = request.data.get(u'currencyIn')
        currency_out = request.data.get(u'currencyOut')
        start_date = dateutil.parser.parse(str(start_date).replace('"', ''))
        end_date = dateutil.parser.parse(str(end_date).replace('"', ''))

        start_date = start_date.date()
        end_date = end_date.date()

        graph_data = CurrencyExchange.objects.filter(currency_code_in=currency_in)\
            .filter(currency_code_out=currency_out)\
            .filter(exchange_rate_on__range=(start_date,end_date))

        graph_data = [data.get_graph_obj() for data in graph_data]

        return Response({
            'data':{
                'graphData': graph_data
            },
            'success': True
        }, status=status.HTTP_200_OK)



