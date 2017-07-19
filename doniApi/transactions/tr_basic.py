from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import Transaction, TrCommission, BpBasic, ProductItem, \
    Packaging, CommissionType, TrShipment, TransactionChangeLog, TrWashout, TrComplete
from datetime import datetime as dt
import dateutil.parser
from rest_framework.permissions import IsAuthenticated, AllowAny
import dateutil.parser
from notifications.signals import notify



class TransactionDropDownAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user=request.user
        print request.get
        return Response({
            'transactionList': []
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


            print washout.get_description_obj()

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



class TransactionListAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        business = user.profile.business
        start_date = request.GET.get(u'startDate')
        end_date = request.GET.get(u'endDate')
        start_date = dateutil.parser.parse(str(start_date).replace('"', ''))
        end_date = dateutil.parser.parse(str(end_date).replace('"', ''))
        all_transactions = Transaction.objects.filter(date__gte=start_date.date(), date__lte=end_date.date()) \
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




