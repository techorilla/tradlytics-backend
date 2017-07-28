from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import Transaction, TrComplete
permission_classes = (IsAuthenticated,)


class TransactionArrivedNotCompletedListAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        arrived_at_port_not_completed = Transaction.get_arrived_at_port_not_completed()
        return Response({
            'arrivedNotCompletedList':[]
        })




class TransactionDashboardAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):


        return Response({
            'dashboardData': self.get_trade_dashboard_data(request.user)
        }, status=status.HTTP_200_OK)


    def get_trade_dashboard_data(self, user):
        # Count of trades
        business = user.profile.business
        business_trades = Transaction.objects.filter(created_by__profile__business=business)
        total_trades = business_trades.count()
        total_completed_trades = TrComplete.objects.filter(transaction__created_by__profile__business=user.profile.business)\
            .filter(is_complete=True)
        total_completed_trades = total_completed_trades.count()

        # Trades Arrived At Port But Not Complete

        arrived_at_port_not_completed = Transaction.get_arrived_at_port_not_completed(business)
        arrived_at_port_not_completed_count = arrived_at_port_not_completed.count()

        # Trades Shipped Expected Arrival

        expected_arrival = Transaction.get_expected_arrival(business)
        expected_arrival_count = expected_arrival.count()

        #Trades Not Shipped

        not_shipped = Transaction.get_not_shipped_not_washout_not_completed(business)
        not_shipped_count = not_shipped.count()


        return {
            'tradesCount': {
                'total': total_trades,
                'completed': total_completed_trades,
                'percentageCompleted': (float(total_completed_trades)/float(total_trades)) * 100
            },
            'arrivedNotCompletedCount': arrived_at_port_not_completed_count,
            'expectedArrivalCount': expected_arrival_count,
            'notShippedCount': not_shipped_count
        }

