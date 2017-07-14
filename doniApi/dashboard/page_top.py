from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import Transaction



class PageTopSearchAPI(GenericAPIView):

    SEARCH_QUERY_TYPE = {
        'int_trade_file_id':{
            'model': Transaction,
            'field': 'file_id',
            'query': 'istartswith',
            'resultType': 'intFile',
            'resultFields': ['file_id', 'contract_id', 'shipment__bl_no']
        },
        'int_trade_bl_no':{
            'model': Transaction,
            'field': 'shipment__bl_no',
            'query': 'istartswith',
            'resultType': 'intFile',
            'resultFields': ['file_id', 'contract_id', 'shipment__bl_no']
        },
        'int_trade_contract_id':{
            'model': Transaction,
            'field': 'contract_id',
            'query': 'istartswith',
            'resultType': 'intFile',
            'resultFields': ['file_id', 'contract_id', 'shipment__bl_no']
        }
        # 'int_trade_invoice_no':{
        #     'model': Transaction,
        #     'field':None,
        #     'query': 'istartswith',
        #     'resultType': 'intFile'
        # }

    }

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        query_type = str(request.GET.get('queryType'))
        query_str =  str(request.GET.get('query'))
        print query_type, query_str
        query_config = self.SEARCH_QUERY_TYPE[query_type]
        model = query_config['model']

        result_list = model.objects.filter(**{query_config['field']+'__'+query_config['query']:query_str})\
            .values(*query_config['resultFields'])

        return Response( {
            'resultList': result_list,
            'resultType': query_config['resultType'],
            'success': True,
        }, status=status.HTTP_200_OK)