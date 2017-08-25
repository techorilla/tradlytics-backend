from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import Transaction, TrCommission, BpBasic, ProductItem, \
    Packaging, CommissionType, TrShipment, TransactionChangeLog, TrWashout, TrComplete, SecondaryTrades, PartialShipments
from datetime import datetime as dt
import dateutil.parser
from rest_framework.permissions import IsAuthenticated, AllowAny
import dateutil.parser
from notifications.signals import notify
from django.db.models.functions import Concat
from django.db.models import Q, F, Case, When, Value, BooleanField
import operator
from doniCore.utils import get_days_ago

QUERY_MAPPING = {
    'id':'tr_id',
    'date': 'date',
    'rate':'price',
    'quantity':'quantity',
    'shipmentStart':'shipment_start',
    'shipmentEnd':'shipment_end',
    'productName':'product_item__product_origin__product__name',
    'buyerName': 'buyer__bp_name',
    'buyerId': 'buyer__bp_id',
    'sellerId': 'seller__bp_id',
    'productItemId': 'product_item__id',
    'sellerName': 'seller__bp_name',
    'fileNo':'file_id',
    'expectedCommission': 'commission__expected_commission',
    'actualCommission': 'commission__actual_commission',
    'productOriginName': 'product_item__product_origin__country_name',
    'productOriginFlag': 'product_item__product_origin__country_flag',
    'buyerCountry': 'buyer__locations__country_name',
    'sellerCountry': 'seller__locations__country_name',
    'expiredSince': 'expiredSince',
    'contractNo': 'contract_id',
    'blNo':'shipment__bl_no',
    'dateArrived': 'shipment__date_arrived',
    'expectedArrival': 'shipment__expected_arrival',
    'shipmentExpiration': 'shipment_end',
    'disputedOn': 'dispute__dispute_date',
    'completedOn': 'completion_status__completion_date',
    'status': 'status'
}


def get_business_location_query(business_type):
    location_query = [
        (business_type + '__locations__is_primary', True),
        (business_type + '__locations__isnull', True)
    ]
    location_query_list = [Q(query) for query in location_query]
    return reduce(operator.or_, location_query_list)

BUSINESS_ANALYTICS = {
    'columns': [
        'id',
        'date',
        'fileNo',
        'productName',
        'buyerName',
        'buyerId',
        'sellerName',
        'sellerId',
        'productItemId',
        'quantity',
        'rate',
        'productOriginName',
        'productOriginFlag',
        'expectedCommission',
        'actualCommission'
    ],
    'order_by':'-date',
}


TRADE_BOOK_LIST = {
    'columns': [
        'id',
        'date',
        'fileNo',
        'productName',
        'buyerName',
        'buyerId',
        'sellerName',
        'sellerId',
        'productItemId',
        'quantity',
        'rate',
        'productOriginName',
        'productOriginFlag',
        'shipmentStart',
        'shipmentEnd',
        'status'
    ],
    'query_columns':{
        'buyerCountry': get_business_location_query('buyer'),
        'sellerCountry': get_business_location_query('seller')
    },
    'restricted_columns':[
        {
            'right': 'right_business_commission',
            'columns':[
                'expectedCommission',
                'actualCommission'
            ],
            'column_header': [
                {
                    'name':'Expected Commission  <span class=\'titled\'>USD</span>',
                    'sort': 'expectedCommission'
                },
                {
                    'name':'Actual Commission  <span class=\'titled\'>USD</span>',
                    'sort': 'actualCommission'
                },

            ]

        }
    ],
    'order_by':'-date',
    'column_header': [
        {'name':'Date', 'sort':'date'},
        {'name':'File No', 'sort':'fileNo'},
        {'name':'Buyer', 'sort':'buyerName'},
        {'name':'Product', 'sort':'productName'},
        {'name':'Origin', 'sort':'productOriginName'},
        {'name':'Quantity <span class=\'titled\'>MT</span>', 'sort':'quantity'},
        {'name':'Rate <span class=\'titled\'>USD</span>', 'sort':'rate'},
        {'name':'Seller', 'sort':'sellerName'},
        {'name':'Shipment Start', 'sort':'shipmentStart'},
        {'name':'Shipment End', 'sort':'shipmentEnd'}
    ]
}


ARRIVED_LIST = {
    'columns': [
        'id',
        'fileNo',
        'productName',
        'buyerName',
        'buyerId',
        'sellerName',
        'sellerId',
        'productItemId',
        'quantity',
        'rate',
        'productOriginName',
        'productOriginFlag',
        'contractNo',
        'blNo',
        'dateArrived'
    ],
    'query_columns':{
        'buyerCountry': get_business_location_query('buyer'),
        'sellerCountry': get_business_location_query('seller')
    },
    'order_by':'-shipment__date_arrived',
    'column_header': [
        {'name':'Date Arrived', 'sort':'dateArrived'},
        {'name':'Arrived Since', 'sort':None},
        {'name': 'File No', 'sort': 'fileNo'},
        {'name':'BL No.', 'sort':'blNo'},
        {'name':'Contract No.', 'sort':'contractNo'},
        {'name':'Buyer', 'sort':'buyerName'},
        {'name':'Product', 'sort':'productName'},
        {'name':'Origin', 'sort':'productOriginName'},
        {'name':'Seller', 'sort':'sellerName'},
        {'name':'Quantity <span class=\'titled\'>MT</span>', 'sort':'quantity'},
        {'name':'Rate <span class=\'titled\'>USD</span>', 'sort':'rate'}
    ]
}

EXPECTED_ARRIVAL_LIST = {
    'order_by':'-expectedArrival',
    'columns': [
        'id',
        'fileNo',
        'productName',
        'buyerName',
        'buyerId',
        'sellerName',
        'sellerId',
        'productItemId',
        'quantity',
        'rate',
        'productOriginName',
        'productOriginFlag',
        'contractNo',
        'blNo',
        'expectedArrival'
    ],
    'query_columns':{
        'buyerCountry': get_business_location_query('buyer'),
        'sellerCountry': get_business_location_query('seller')
    },
    'column_header': [
        {'name': 'Expected Arrival', 'sort': 'expectedArrival'},
        {'name': 'Expected Since', 'sort': None},
        {'name': 'File No', 'sort': 'fileNo'},
        {'name': 'BL No.', 'sort': 'blNo'},
        {'name': 'Contract No.', 'sort': 'contractNo'},
        {'name': 'Buyer', 'sort': 'buyerName'},
        {'name': 'Product', 'sort': 'productName'},
        {'name': 'Origin', 'sort': 'productOriginName'},
        {'name': 'Seller', 'sort': 'sellerName'},
        {'name': 'Quantity <span class=\'titled\'>MT</span>', 'sort': 'quantity'},
        {'name': 'Rate <span class=\'titled\'>USD</span>', 'sort': 'rate'}
    ]
}

SHIPMENT_EXPIRATION_LIST = {
    'columns': [
        'id',
        'fileNo',
        'productName',
        'buyerName',
        'buyerId',
        'sellerName',
        'sellerId',
        'productItemId',
        'quantity',
        'rate',
        'productOriginName',
        'productOriginFlag',
        'contractNo',
        'blNo',
        'shipmentExpiration'
    ],
    'order_by': '-shipmentExpiration',
    'query_columns':{
        'buyerCountry': get_business_location_query('buyer'),
        'sellerCountry': get_business_location_query('seller')
    },
    'column_header': [
        {'name': 'Expired On', 'sort': 'shipmentExpiration'},
        {'name': 'Expired Since', 'sort': None},
        {'name': 'File No', 'sort': 'fileNo'},
        {'name': 'BL No.', 'sort': 'blNo'},
        {'name': 'Contract No.', 'sort': 'contractNo'},
        {'name': 'Buyer', 'sort': 'buyerName'},
        {'name': 'Product', 'sort': 'productName'},
        {'name': 'Origin', 'sort': 'productOriginName'},
        {'name': 'Seller', 'sort': 'sellerName'},
        {'name': 'Quantity <span class=\'titled\'>MT</span>', 'sort': 'quantity'},
        {'name': 'Rate <span class=\'titled\'>USD</span>', 'sort': 'rate'}
    ]
}

TRADE_DISPUTE = {
    'columns': [
        'id',
        'fileNo',
        'disputedOn',
        'completedOn',
        'productName',
        'buyerName',
        'buyerId',
        'sellerName',
        'sellerId',
        'productItemId',
        'quantity',
        'rate',
        'productOriginName',
        'productOriginFlag',
        'contractNo',
    ],
    'order_by': '-disputedOn',
    'query_columns':{
        'buyerCountry': get_business_location_query('buyer'),
        'sellerCountry': get_business_location_query('seller')
    },
    'column_header': [
        {'name': 'Disputed On', 'sort': 'disputedOn'},
        {'name': 'Disputed Since', 'sort': None},
        {'name': 'File No', 'sort': 'fileNo'},
        {'name': 'Contract No.', 'sort': 'contractNo'},
        {'name': 'Completed On', 'sort': 'completedOn'},
        {'name': 'Buyer', 'sort': 'buyerName'},
        {'name': 'Product', 'sort': 'productName'},
        {'name': 'Origin', 'sort': 'productOriginName'},
        {'name': 'Seller', 'sort': 'sellerName'},
        {'name': 'Quantity <span class=\'titled\'>MT</span>', 'sort': 'quantity'},
        {'name': 'Rate <span class=\'titled\'>USD</span>', 'sort': 'rate'}
    ]
}

TRANSACTION_LIST_CONFIG = {
    'tradeBook': TRADE_BOOK_LIST,
    'expectedArrival': EXPECTED_ARRIVAL_LIST,
    'arrivedList': ARRIVED_LIST,
    'expiredShipment': SHIPMENT_EXPIRATION_LIST,
    'businessAnalytics': BUSINESS_ANALYTICS,
    'tradeDispute': TRADE_DISPUTE
}








class TransactionListReportAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user=request.user
        business = user.profile.business





class TransactionListAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_transaction_list(queryset, page_type, user):
        page_config = TRANSACTION_LIST_CONFIG[page_type]
        values = list()
        annotate_obj = dict()
        column_header = []
        for column in page_config['columns']:
            query_map = QUERY_MAPPING[column]
            values.append(query_map)
            if column != query_map:
                annotate_obj[column] = F(query_map)
        column_header = page_config['column_header']
        restricted = page_config.get('restricted_columns', [])

        for restrict in restricted:
            if getattr(user.profile, restrict['right']):
                for column in restrict['columns']:
                    query_map = QUERY_MAPPING[column]
                    values.append(query_map)
                    if column != query_map:
                        annotate_obj[column] = F(query_map)
                column_header = column_header + restrict['column_header']

        query_columns = page_config.get('query_columns', [])

        for column, query in query_columns.items():
            values.append(QUERY_MAPPING[column])
            if column != query_map:
                annotate_obj[column] = F(QUERY_MAPPING[column])
                queryset = queryset.filter(query)

        # annotate_columns = page_config.get('annotate_columns', {})
        # for column, annotation in annotate_columns.items():
        #     values.append(QUERY_MAPPING[column])
        #     if column != query_map:
        #         annotate_obj[column] = annotation


        queryset = queryset.values(*values).annotate(**annotate_obj) \
            .annotate(
            isSecondary=Case(
                When(secondary_trade__isnull=False,
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField())
        ) \
            .annotate(
            hasSecondary=Case(
                When(primary_trade__gt=0,
                     then=Value(True)),
                default=Value(False),
                output_field=BooleanField())
        )
        return queryset.distinct().order_by(*[page_config['order_by']]), column_header

    def get(self, request, *args, **kwargs):
        user = request.user
        business = user.profile.business
        page_type = request.GET.get(u'pageType')

        start_date = request.GET.get(u'startDate')
        end_date = request.GET.get(u'endDate')

        if page_type == 'tradeBook':
            if end_date and start_date:
                start_date = dateutil.parser.parse(str(start_date).replace('"', ''))
                end_date = dateutil.parser.parse(str(end_date).replace('"', ''))
                all_transaction = Transaction.get_trades_in_date_range(business, start_date, end_date)
            else:
                all_transaction = Transaction.objects
            all_transaction = Transaction.get_status(all_transaction)
        elif page_type == 'expectedArrival':
            all_transaction = Transaction.get_expected_arrival(business)
        elif page_type == 'tradeDispute':
            all_transaction = Transaction.get_business_all_disputed_trades(business)
        elif page_type == 'arrivedList':
            all_transaction = Transaction.get_arrived_at_port_not_completed(business)
        elif page_type == 'expiredShipment':
            all_transaction = Transaction.get_not_shipped_not_washout_not_completed(business)

        all_transaction, column_header = self.get_transaction_list(all_transaction, page_type, user)

        return Response({
            'success': True,
            'columnHeader': column_header,
            'transactions': all_transaction
        }, status=status.HTTP_200_OK)

class TransactionWashoutAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        try:

            base_url = request.META.get('HTTP_HOST')
            user = request.user
            washout_data = request.data.get('washOut')
            initial_commission_payable = washout_data.get('initialCommissionPayable')

            is_washout = washout_data.get('isWashout')
            buyer_washout_price = washout_data.get('buyerWashoutPrice')
            seller_washout_price = washout_data.get('sellerWashoutPrice')
            broker_difference = washout_data.get('brokerDifference')
            washout_date = washout_data.get('washoutDate')
            washout_due_date = washout_data.get('washoutDueDate')

            if is_washout:
                washout_date = dateutil.parser.parse(washout_date)
                washout_due_date = dateutil.parser.parse(washout_due_date)
                washout_date = washout_date.replace(hour=0, minute=0, second=0, microsecond=0)
                washout_due_date = washout_due_date.replace(hour=0, minute=0, second=0, microsecond=0)

            transaction_id = request.data.get('transactionId')
            transaction = Transaction.objects.get(tr_id=transaction_id)

            if hasattr(transaction, 'washout'):
                washout = transaction.washout
                washout.updated_by = user
                if washout:
                    message = 'Transaction Washout Details Updated Successfully!'
                else:
                    message = 'Transaction Washout Status Deactivated Successfully!'
            else:
                washout = TrWashout()
                washout.transaction = transaction
                washout.created_by = user
                washout.updated_at = dt.now()
                message = 'Transaction Washout Status Activated Successfully!'

            washout.initial_commission_payable = initial_commission_payable
            washout.washout_date = washout_date
            washout.washout_due_date = washout_due_date
            washout.is_washout = is_washout
            washout.buyer_washout_price = float(buyer_washout_price.replace(',',''))
            washout.seller_washout_price = float(seller_washout_price.replace(',',''))
            washout.broker_difference = float(broker_difference.replace(',',''))
            washout.save()

            return Response({
                'transactionObj': transaction.get_complete_obj(base_url, user),
                'success': True,
                'message': message
            })
        except Exception, e:
            print str(e)
            return Response({
                'success': False,
                'message': str(e)
            })

class TransactionCompleteStatusAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            base_url = request.META.get('HTTP_HOST')
            user = request.user
            data = request.data
            transaction_id = data.get('transactionId')
            transaction = Transaction.objects.get(tr_id=transaction_id)

            complete_obj = data.get('completeObj')

            if hasattr(transaction, 'completion_status'):
                transaction_completion = transaction.completion_status
                transaction_completion.updated_by = user
                transaction_completion.updated_at = dt.now()
            else:
                transaction_completion = TrComplete()
                transaction_completion.created_by = user
                transaction_completion.transaction = transaction


            transaction_completion.is_complete = complete_obj.get('complete')
            completion_date = complete_obj.get('completionDate')
            if completion_date:
                completion_date = dateutil.parser.parse(str(completion_date).replace('"', ''))
                completion_date = completion_date.replace(hour=0, minute=0, second=0, microsecond=0)

            transaction_completion.completion_date = completion_date
            transaction_completion.save()


            #TODO: MOVE TO SIGNAL
            if  complete_obj.get('complete'):
                message = 'Transaction completed successfully.'
            else:
                message = 'Transaction status changed to incomplete successfully.'

            return Response({
                'transactionObj': transaction.get_complete_obj(base_url, user),
                'success': True,
                'message': message
            })
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })





class TransactionBasicAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    messages = dict()

    messages['successPOST'] = 'Transaction File %s created successfully.'
    messages['successPUT'] = 'Transaction File %s updated successfully.'

    def get(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        user = request.user
        file_id = request.GET.get('tradeId')
        full_obj = request.GET.get('full')
        transaction = Transaction.objects.get(file_id=file_id)
        if full_obj:
            transaction = transaction.get_complete_obj(base_url, user)
        else:
            transaction = transaction.get_obj()
        return Response({
            'transaction': transaction,
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        return self.save_transaction(data, request.user)

    def save_transaction(self, data, user):
        try:
            tran_id = data.get('id')
            product_specs = data.get('productSpecification')
            commission_data = data.get('commission')
            basic = data.get('basic')
            buyer_id = basic.get('buyerId')
            contractual_buyer_id = basic.get('contractualBuyerId')
            seller_id = basic.get('sellerId')
            packaging_id = basic.get('packagingId')
            product_item_id = basic.get('productItemId')


            transaction_date = dateutil.parser.parse(str(basic.get('date')).replace('"', ''))
            transaction_date =  transaction_date.replace(hour=0, minute=0, second=0, microsecond=0)

            shipment_start = dateutil.parser.parse(str(basic.get('shipmentStart')).replace('"', ''))
            shipment_start = shipment_start.replace(hour=0, minute=0, second=0, microsecond=0)

            shipment_end = dateutil.parser.parse(str(basic.get('shipmentEnd')).replace('"', ''))
            shipment_end = shipment_end.replace(hour=0, minute=0, second=0, microsecond=0)


            packaging = Packaging.objects.get(id=packaging_id)
            commission_type_id = commission_data.get('typeId')
            seller_broker_id = commission_data.get('sellerBrokerId')
            buyer_broker_id = commission_data.get('buyerBrokerId')
            buyer_broker_commission_type_id = commission_data.get('buyerBrokerCommissionTypeId')

            if buyer_id == seller_id:
                return Response({
                    'success': False,
                    'message': 'Buyer and Seller can not be same'
                })
            buyer = BpBasic.objects.get(bp_id=buyer_id)
            seller = BpBasic.objects.get(bp_id=seller_id)
            product_item = ProductItem.objects.get(id=product_item_id)
            contractual_buyer = BpBasic.objects.get(bp_id=contractual_buyer_id)
            commission_type = CommissionType.objects.get(id=commission_type_id)
            buyer_broker_commission_type = None if not buyer_broker_id else CommissionType.objects.get(id=buyer_broker_commission_type_id)
            seller_broker = None if not seller_broker_id else BpBasic.objects.get(bp_id=seller_broker_id)
            buyer_broker = None if not buyer_broker_id else BpBasic.objects.get(bp_id=buyer_broker_id)


            #update
            if tran_id:
                success_message = self.messages['successPUT']
                transaction = Transaction.objects.get(tr_id=tran_id)
                commission = TrCommission.objects.get(transaction__tr_id=tran_id)
                transaction.updated_by = user
                transaction.updated_at = dt.now()

            #add
            else:
                success_message = self.messages['successPOST']
                transaction = Transaction()
                commission = TrCommission()
                transaction.created_by = user



            # saving all transaction details
            transaction.seller = seller
            transaction.buyer = buyer
            transaction.product_item = product_item
            transaction.contractual_buyer = contractual_buyer
            transaction.other_info = basic.get('otherInfo')
            transaction.file_id = basic.get('fileId')
            transaction.contract_id = basic.get('contractId')
            transaction.product_specification = product_specs
            transaction.shipment_start = shipment_start.date()
            transaction.shipment_end = shipment_end.date()
            transaction.price = float(basic.get('price'))
            transaction.quantity = float(basic.get('quantity'))
            transaction.quantity_fcl = float(basic.get('quantityFcl'))
            transaction.date = transaction_date.date()
            transaction.packaging = packaging
            # saving all commission details
            commission.discount = float(commission_data.get('discount'))
            commission.difference = float(commission_data.get('difference'))
            commission.commission = float(commission_data.get('commission'))
            commission.commission_type = commission_type
            commission.seller_broker = seller_broker
            commission.buyer_broker = buyer_broker
            commission.buyer_broker_comm_type = buyer_broker_commission_type
            commission.buyer_broker_comm = float(commission_data.get('buyerBrokerCommission', 0.00))
            transaction.save()
            commission.transaction = transaction
            commission.save()

            # Assigning not shipped status to new transaction
            if not tran_id:
                shipment = TrShipment()
                shipment.transaction = transaction
                shipment.not_shipped = True
                shipment.created_by = user
                shipment.save()

            primary_transaction_id = basic.get('primaryTransaction')
            primary_shipment_id = basic.get('primaryShipment')



            if primary_transaction_id:
                primary_transaction = Transaction.objects.get(file_id=primary_transaction_id)
                if hasattr(transaction, 'secondary_trade'):
                    secondary_trade = transaction.secondary_trade
                else:
                    secondary_trade = SecondaryTrades()
                secondary_trade.transaction = transaction
                secondary_trade.primary_trade = primary_transaction
                secondary_trade.save()
            else:
                if hasattr(transaction, 'secondary_trade'):
                    transaction.secondary_trade.delete()




            if primary_shipment_id:
                primary_shipment = Transaction.objects.get(file_id=primary_shipment_id)
                if hasattr(transaction, 'partial_shipment'):
                    partial_shipment = transaction.partial_shipment
                else:
                    partial_shipment = PartialShipments()
                partial_shipment.transaction = transaction
                partial_shipment.primary_shipment = primary_shipment
                partial_shipment.save()
            else:
                if hasattr(transaction, 'partial_shipment'):
                    transaction.primary_trade.all().delete()





            # Making Transaction Change Log

            if tran_id:
                #TODO: Have to make detail log message
                log = '<span class="titled">Updated Transaction</span>'
                TransactionChangeLog.add_change_log(user, log, transaction)
            else:
                log = '<span class="titled">Created Transaction</span>'
                TransactionChangeLog.add_change_log(user, log, transaction)

            return Response({
                'fileId': transaction.file_id,
                'success': True,
                'message': success_message % transaction.file_id
            }, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })




    def delete(self, request, *args, **kwargs):
        return Response()

    def put(self, request, *args, **kwargs):
        data = request.data
        return self.save_transaction(data, request.user)




