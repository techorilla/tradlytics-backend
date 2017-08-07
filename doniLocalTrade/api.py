from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import LocalTrade, LocalTradeChangeLog, LocalTradeNotes, LocalTradeStatus, PaymentTerm, DeliverySlip
from datetime import datetime as dt
from django.db.models import Sum, Count
import dateutil.parser


class LocalTradeAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

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



