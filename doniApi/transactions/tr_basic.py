from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import Transaction, TrCommission, BpBasic, ProductItem, Packaging, CommissionType
from datetime import datetime as dt
import dateutil.parser
from rest_framework.permissions import IsAuthenticated, AllowAny


class TransactionListAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        business = user.profile.business
        start_date = request.GET.get(u'startDate')
        end_date = request.GET.get(u'endDate')
        start_date = dateutil.parser.parse(str(start_date).replace('"', ''))
        end_date = dateutil.parser.parse(str(end_date).replace('"', ''))
        all_transactions = Transaction.objects.filter(date__gte=start_date.date(), date__lte=end_date.date())\
            .filter(created_by__profile__business=business).order_by('-date')
        all_transactions = [trade.get_list_object() for trade in all_transactions]
        return Response({
            'success': True,
            'transactions': all_transactions
        }, status=status.HTTP_200_OK)


class TransactionBasicAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    messages = dict()

    messages['successPOST'] = 'Transaction File %s created successfully.'
    messages['successPUT'] = 'Transaction File %s updated successfully.'

    def get(self, request, *args, **kwargs):
        transation_id = request.GET.get('tr_id')
        transaction = Transaction.objects.get(tr_id=transaction)
        return Response({
            'transaction': []
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
            shipment_start = dateutil.parser.parse(str(basic.get('shipmentStart')).replace('"', ''))
            shipment_end = dateutil.parser.parse(str(basic.get('shipmentEnd')).replace('"', ''))
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
            buyer_broker_commission_type = CommissionType.objects.get(id=buyer_broker_commission_type_id)
            seller_broker = None if not seller_broker_id else BpBasic.objects.get(bp_id=seller_broker_id)
            buyer_broker = None if not buyer_broker_id else BpBasic.objects.get(bp_id=buyer_broker_id)
            net_commission = data.get('netCommission')

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
            transaction.date = transaction_date.date()
            transaction.packaging = packaging
            # saving all commission details
            commission.net_commission = float(net_commission)
            commission.discount = float(commission_data.get('discount'))
            commission.difference = float(commission_data.get('difference'))
            commission.commission = float(commission_data.get('commission'))
            commission.commission_type = commission_type
            commission.seller_broker = seller_broker
            commission.buyer_broker = buyer_broker
            commission.buyer_broker_comm_type = buyer_broker_commission_type
            commission.buyer_broker_comm = float(commission_data.get('buyerBrokerCommission'))
            transaction.save()
            commission.transaction = transaction
            commission.save()

            return Response({
                'tradeId': transaction.tr_id,
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
        return self.save_transaction(data, request.user)




