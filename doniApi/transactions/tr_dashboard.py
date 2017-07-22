from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import Transaction, TrComplete
permission_classes = (IsAuthenticated,)




class TransactionDashboardAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):


        return Response({
            'dashboardData': self.get_trade_dashboard_data(request.user)
        }, status=status.HTTP_200_OK)


    def get_trade_dashboard_data(self, user):

        business_trades = Transaction.objects.filter(created_by__profile__business=user.profile.business)

        total_trades = business_trades.count()
        total_completed_trades = TrComplete.objects.filter(transaction__created_by__profile__business=user.profile.business).filter(is_complete=True)
        total_completed_trades = total_completed_trades.count()

        return {
            'tradesCount': {
                'total': total_trades,
                'completed': total_completed_trades,
                'percentageCompleted': (float(total_completed_trades)/float(total_trades)) * 100
            }
        }

