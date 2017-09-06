from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import Transaction
from .models import LocalTrade, LocalTradeChangeLog, LocalTradeNotes, LocalTradeStatus, PaymentTerm, DeliverySlip,\
                    AssociatedLocalTrade, AssociatedInternationalTrade, LocalTradePayment
from datetime import datetime as dt
from django.db.models import Q, F
import operator
from django.db.models import Sum, Count
import dateutil.parser


class LocalTradeAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def save_local_trade(self, request):
        try:
            method = request.method
            user = request.user
            data = request.data
            local_trade_id = data.get('id')
            payment_term = data.get('paymentTerm')
            other_info = data.get('otherInfo')
            delivery_due_date = data.get('deliveryDueDate')
            funds_due_date = data.get('fundsDueDate')
            contract_id = data.get('contractId')
            payment_date = data.get('paymentDate')
            quantity_fcl = data.get('quantityFCL')
            local_trade_associated = data.get('localFileId')
            international_trade_associated = data.get('internationalFileId')


            date = data.get('date')
            date = dateutil.parser.parse(str(date).replace('"', ''))
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)

            buyer_id = data.get('buyerId')
            seller_id = data.get('sellerId')
            file_id = data.get('fileId')
            product_id = data.get('productItemId')
            quantity = data.get('quantity')
            price = data.get('price')

            if float(price) == 0.00:
                return Response({
                    'success': False,
                    'message': 'Price can not be zero.'
                })

            if float(quantity) == 0.00:
                return Response({
                    'success': False,
                    'message': 'Quantity can not be zero.'
                })

            if int(seller_id) == int(buyer_id):
                return Response({
                    'success': False,
                    'message': 'Buyer and Seller can not be same.'
                })

            local_trade_associated = LocalTrade.objects.filter(file_id__in=local_trade_associated)
            international_trade_associated = Transaction.objects.filter(file_id__in=international_trade_associated)

            if method == 'POST':
                local_trade = LocalTrade()
                local_trade.business = user.profile.business
                local_trade.created_by = user
            elif method == 'PUT':
                local_trade = LocalTrade.objects.get(business=user.profile.business, file_id=str(file_id))
                local_trade.associated_local_trade.all().delete()
                local_trade.associated_international_trade.all().delete()
                local_trade.updated_by = user
                local_trade.updated_on = dt.now()



            local_trade.date = date
            local_trade.local_buyer_id = buyer_id
            local_trade.local_seller_id = seller_id
            local_trade.file_id = file_id
            local_trade.contract_id = contract_id
            local_trade.price = price
            local_trade.quantity = quantity
            local_trade.quantity_fcl = quantity_fcl
            local_trade.other_info = other_info
            local_trade.product_item_id = product_id
            local_trade.save()

            for trade in local_trade_associated:
                ass_trade = AssociatedLocalTrade()
                ass_trade.local_trade = local_trade
                ass_trade.local_trade_associated = trade
                ass_trade.save()

            for transaction in international_trade_associated:
                ass_trade = AssociatedInternationalTrade()
                ass_trade.local_trade = local_trade
                ass_trade.transaction_associated = transaction
                ass_trade.save()


            PaymentTerm.ls\
                (local_trade, payment_term, payment_date)
            LocalTradeStatus.save_delivery_due_date(local_trade, delivery_due_date, funds_due_date)

            return Response({
                'success': True,
                'message': 'Local Trade with file id %s saved successfully'%file_id
            })
        except Exception,e:
            import traceback
            print traceback.format_exc()
            print str(e)

    def put(self, request, *args, **kwargs):
        return self.save_local_trade(request)

    def post(self, request, *args, **kwargs):
        return self.save_local_trade(request)

    def get(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        print 'here i am this is me'
        user = request.user
        file_id = request.GET.get('tradeId')
        full_obj = request.GET.get('full')
        local_trade = LocalTrade.objects.get(file_id=file_id)

        if full_obj:
            local_trade = local_trade.get_complete_obj(base_url, user)
        else:
            local_trade = local_trade.get_obj()
        return Response({
            'localTrade': local_trade
        }, status=status.HTTP_200_OK)

# Local Trade List API

def get_business_location_query(business_type):
    location_query = [
        (business_type + '__locations__is_primary', True),
        (business_type + '__locations__isnull', True)
    ]
    location_query_list = [Q(query) for query in location_query]
    return reduce(operator.or_, location_query_list)

QUERY_MAPPING = {
    'id':'id',
    'date': 'date',
    'rate':'price',
    'quantity':'quantity',
    'quantity_fcl': 'quantity_fcl',
    'productName':'product_item__product_origin__product__name',
    'buyerName': 'local_buyer__bp_name',
    'buyerId': 'local_buyer__bp_id',
    'sellerId': 'local_seller__bp_id',
    'productItemId': 'product_item__id',
    'sellerName': 'local_seller__bp_name',
    'fileNo':'file_id',
    'productOriginName': 'product_item__product_origin__country_name',
    'productOriginFlag': 'product_item__product_origin__country_flag',
    'buyerCountry': 'local_buyer__locations__country_name',
    'sellerCountry': 'local_seller__locations__country_name',
    'contractNo': 'contract_id',
    'internationalFileId': 'international_file__tr_id',
    'internationalFileNo': 'international_file__file_id',
    'deliveryDueDate': 'status__delivery_due_date',
    'fundsDueDate': 'status__funds_due_date'
}

TRADE_BOOK_LIST = {
    'columns': [
        'id',
        'date',
        'fileNo',
        'buyerName',
        'buyerId',
        'sellerName',
        'sellerId',
        'productItemId',
        'productName',
        'quantity',
        'rate',
        'productOriginName',
        'productOriginFlag',
        'fundsDueDate',
        'deliveryDueDate'
    ],
    'order_by': '-date',
    'query_columns':{
        'buyerCountry': get_business_location_query('local_buyer'),
        'sellerCountry': get_business_location_query('local_seller')
    },
    'column_header': [
        {'name':'Date', 'sort':'date'},
        {'name':'File No', 'sort':'fileNo'},
        {'name':'Buyer', 'sort':'buyerName'},
        {'name':'Product', 'sort':'productName'},
        {'name':'Origin', 'sort':'productOriginName'},
        {'name':'Quantity <span class=\'titled\'>MT</span>', 'sort':'quantity'},
        {'name':'Rate <span class=\'titled\'>{{currency}}</span>', 'sort':'rate'},
        {'name':'Seller', 'sort':'sellerName'},
        {'name': 'Delivery Due Date', 'sort': 'deliveryDueDate'},
        {'name': 'Funds Due Date', 'sort': 'fundsDueDate'}
    ]
}

LOCAL_TRADE_LIST_CONFIG = {
    'localTradeBook': TRADE_BOOK_LIST
}


class LocalTradeListAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_transaction_list(queryset, page_type, user):
        page_config = LOCAL_TRADE_LIST_CONFIG[page_type]
        values = list()
        annotate_obj = dict()
        for column in page_config['columns']:
            query_map = QUERY_MAPPING[column]
            values.append(query_map)
            if column != query_map:
                annotate_obj[column] = F(query_map)
        column_header = page_config['column_header']
        query_columns = page_config.get('query_columns', [])

        for column, query in query_columns.items():
            query_map = QUERY_MAPPING[column]
            values.append(query_map)
            if column != query_map:
                annotate_obj[column] = F(QUERY_MAPPING[column])
                queryset = queryset.filter(query)

        return queryset.values(*values).annotate(**annotate_obj)\
                   .order_by(*[page_config['order_by']]), column_header


    def get(self, request, *args, **kwargs):
        user = request.user
        business = user.profile.business
        page_type = request.GET.get(u'pageType')
        start_date = request.GET.get(u'startDate')
        end_date = request.GET.get(u'endDate')

        if end_date and start_date:
            start_date = dateutil.parser.parse(str(start_date).replace('"', ''))
            end_date = dateutil.parser.parse(str(end_date).replace('"', ''))

        if page_type == 'localTradeBook':
            all_transaction = LocalTrade.get_trades_in_date_range(business, start_date, end_date)

        all_transaction, column_header = self.get_transaction_list(all_transaction, page_type, user)

        for column in column_header:
            column['name'] = column['name'].replace('{{currency}}', business.app_profile.currency)
        return Response({
            'transactions': all_transaction,
            'success': True,
            'columnHeader': column_header
        }, status=status.HTTP_200_OK)

class LocalTradeDashboardAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({

        }, status=status.HTTP_200_OK)

class LocalTradeStatusAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({

        }, status=status.HTTP_200_OK)


class LocalTradePaymentAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        local_trade_id = kwargs.get('file_id')

        return Response({

        }, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        local_trade_id = kwargs.get('file_id')
        payment_id = kwargs.get('payment_id')

        return Response({

        }, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        local_trade_id = kwargs.get('file_id')
        new_payment = LocalTradePayment()

        return Response({

        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response({

        }, status=status.HTTP_200_OK)

class LocalTradeDeliverySlipAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({

        }, status=status.HTTP_200_OK)

# class LocalTrade



