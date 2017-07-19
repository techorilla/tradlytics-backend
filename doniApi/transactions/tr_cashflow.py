from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import Transaction
permission_classes = (IsAuthenticated,)




class TransactionCashFlowAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        print 'hello'
        initial_commission_payable = True
        base_url = request.META.get('HTTP_HOST')
        cash_flow = []
        file_id = request.GET.get(u'fileId')
        transaction = Transaction.objects.get(file_id=file_id)
        washout =  None if not hasattr(Transaction, 'washout') else transaction.washout
        commission = transaction.commission

        if washout:
            initial_commission_payable = washout.initial_commission_payable

        # buyer commission
        if commission.buyer_commission_expected or commission.buyer_commission_actual:
            cash_flow.append({
                'payable': (commission.buyer_commission_actual < 0)  if commission.buyer_commission_actual else (commission.buyer_commission_expected < 0),
                'business': transaction.buyer.get_description_obj(base_url),
                'active': initial_commission_payable,
                'amount': commission.buyer_commission_actual if commission.buyer_commission_actual else commission.buyer_commission_expected,
                'description': 'Transaction Commission From Buyer (Difference / Discount)'
            })

        # seller commission
        cash_flow.append({
            'payable': False,
            'business': transaction.seller.get_description_obj(base_url),
            'active': initial_commission_payable,
            'amount': commission.seller_commission_actual if commission.seller_commission_actual else commission.seller_commission_expected,
            'description': 'Transaction Commission From Seller'
        })

        # Buyer Broker Commission
        if commission.buyer_broker:
            cash_flow.append({
                'payable': True,
                'business': commission.buyer_broker.get_description_obj(base_url),
                'active': initial_commission_payable,
                'amount': commission.buyer_broker_commission_actual if commission.buyer_broker_commission_actual else commission.buyer_broker_commission_actual,
                'description': 'Buyer Broker Commission'
            })

        if washout and washout.washout_commission:
            cash_flow.append({
                'payable': (washout.washout_commission < 0),
                'business': transaction.buyer.get_description_obj(base_url),
                'active': True,
                'amount': washout.washout_commission,
                'description': 'Washout Commission at Difference %.2f * Quantity %.2f MT'%(washout.broker_difference, transaction.quantity)
            })

        return Response({ 'data': {
            'cashFlow': cash_flow,
            'file_id': transaction.file_id
        }})

