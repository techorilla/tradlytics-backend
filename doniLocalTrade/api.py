from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import LocalTrade, LocalTradeChangeLog, LocalTradeNotes, LocalTradeStatus, PaymentTerm, DeliverySlip
from datetime import datetime as dt
from django.db.models import Sum, Count
import dateutil.parser


class LocalTradeAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def save_local_trade(self, request):
        method = request.method
        user = request.user
        data = request.data
        local_trade_id = data.get('id')
        payment_terms = data.get('paymentTerms')
        other_info = data.get('otherInfo')
        delivery_due_date = data.get('deliveryDueDate')
        contract_id = data.get('contractId')
        paymentDate = data.get('paymentDate')
        quantity_fcl = data.get('quantityFCL')
        date = data.get('date')
        data = dateutil.parser.parse(str(date).replace('"', ''))
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        international_file_id = data.get('internationalFileId')
        buyer_id = data.get('buyerId')
        seller_id = data.get('sellerId')
        file_id = data.get('fileId')
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

        if method == 'POST':
            local_trade = LocalTrade()
            local_trade.created_by = user
        elif method == 'PUT':
            local_trade = LocalTrade.objects.get(id=local_trade_id)
            local_trade.updated_by = user
            local_trade.updated_on = dt.now()

        local_trade.date = date
        local_trade.buyer_id = buyer_id
        local_trade.seller_id = seller_id
        local_trade.file_id = file_id
        local_trade.international_file_id = international_file_id
        local_trade.contract_id = contract_id
        local_trade.price = price
        local_trade.quantity = quantity
        local_trade.quantity_fcl = quantity_fcl
        local_trade.save()










    def put(self, request, *args, **kwargs):
        return Response({

        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print request.data
        return Response({

        }, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return Response({

        }, status=status.HTTP_200_OK)


class LocalTradeListAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({

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

class LocalTradeDeliverySlipAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({

        }, status=status.HTTP_200_OK)



