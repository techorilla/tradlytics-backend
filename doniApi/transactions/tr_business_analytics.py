from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .tr_basic import QUERY_MAPPING, TransactionListAPI
import dateutil.parser
from doniServer.models import Transaction


class TransactionBusinessAnalyticsAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        has_business_analytics_access = user.profile.right_business_analytics
        start_date = request.GET.get(u'startDate')
        end_date = request.GET.get(u'endDate')
        start_date = dateutil.parser.parse(str(start_date).replace('"', ''))
        end_date = dateutil.parser.parse(str(end_date).replace('"', ''))
        all_transaction = Transaction.get_trades_in_date_range(business, start_date, end_date)
        all_transaction = TransactionListAPI.get_transaction_list(all_transaction, page_type, user)
        if not has_business_analytics_access:
            return Response({
                success: False,
                message: 'No access for business analytics on you account.'
            })



        return Response({
            'allTransaction': all_transaction
        }, status=status.HTTP_200_OK)
