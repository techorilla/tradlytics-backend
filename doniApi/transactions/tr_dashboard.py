from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import Transaction, TrComplete, SecondaryTrades
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as rd
from django.db.models import Q


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
        business = user.profile.business

        ## Get Get Graph Data

        today = dt.now()
        one_year = today - rd(years=1)
        six_month = today - rd(months=6)
        last_month = today - rd(months=1)
        last_week = today - rd(days=1)

        date_limits = [one_year, six_month, last_month, last_week]

        #New Trades
        new_trades = map(lambda end_date: Transaction.get_trades_in_date_range(business,end_date, today).count(), date_limits)
        #Completed Trades
        complete_trades = map(lambda end_date: Transaction.get_all_business_completed_trades_in_date_range(business, end_date, today).count(), date_limits)

        #Washout Trades
        washout_trades = map(lambda end_date: Transaction.get_all_washout_trades_in_date_range(business, end_date, today).count(), date_limits)

        #Arrived Not Completed Trades

        arrived_trades = map(
            lambda end_date: Transaction.get_arrived_at_port_not_completed_in_date_range(business, end_date, today).count(),
            date_limits)

        #Buyer Contract
        buyer_contract_trades = map(lambda end_date: Transaction.get_buyer_contract_trades_in_date_range(business, end_date, today).count(), date_limits)

        ## Count of trades

        #Total Count
        business_trades = Transaction.objects.filter(created_by__profile__business=business)
        total_trades = business_trades.count()
        total_completed_trades = Transaction.get_all_business_completed_trades(business)
        total_completed_trades = total_completed_trades.count()

        #contract count
        self_contract_count = Transaction.get_self_contract_trades(business).count()
        own_contract_count = total_trades - self_contract_count

        #Washout Count
        washout_count = Transaction.get_business_all_washout(business).count()
        washout_at_x_count = Transaction.objects.filter(created_by__profile__business=business) \
            .filter(washout__total_difference=0.00).count()

        #commissionCount

        fixed_count = Transaction.objects.filter(commission__commission_type__name='Fixed') \
            .filter(created_by__profile__business=user.profile.business).count()
        percentage_count = Transaction.objects.filter(commission__commission_type__name= 'Percentage') \
            .filter(created_by__profile__business=user.profile.business).count()


        # Trades Arrived At Port But Not Complete
        arrived_at_port_not_completed = Transaction.get_arrived_at_port_not_completed(business)
        arrived_at_port_not_completed_count = arrived_at_port_not_completed.count()

        # Trades Shipped Expected Arrival
        expected_arrival = Transaction.get_expected_arrival(business)
        expected_arrival_count = expected_arrival.count()

        #Trades Not Shipped
        not_shipped = Transaction.get_not_shipped_not_washout_not_completed(business)
        not_shipped_count = not_shipped.count()

        #Secondary Trades
        secondary_trades_count = SecondaryTrades.objects.count()
        partial_keys = ['A', 'B', 'C', 'D']
        partial_shipment = Transaction.objects.filter(
            reduce(lambda x, y: x | y, [Q(file_id__icontains=key) for key in partial_keys]))
        partial_shipment_count = partial_shipment.count()


        return {
            'multiBar':{
              'newTrades': new_trades,
              'completeTrades': complete_trades,
              'washoutTrades': washout_trades,
              'arrivedTrades': arrived_trades,
              'buyerContractTrades': buyer_contract_trades
            },
            'tradesCount': {
                'total': total_trades,
                'completed': total_completed_trades,
                'percentageCompleted': (float(total_completed_trades)/float(total_trades)) * 100
            },
            'commissionCount':{
                'fixedCount':fixed_count,
                'percentageCount': percentage_count,
                'percentagePercentageCommission': (float(percentage_count)/float(total_trades)) * 100
            },
            'contractCount':{
                'selfContractCount': self_contract_count,
                'ownContractCount': own_contract_count,
                'percentageOwnContractCount': (float(own_contract_count)/float(total_trades)) * 100
            },
            'washoutCount': {
                'washoutCount': washout_count,
                'washoutAtXCount': washout_at_x_count,
                'washoutPercentage': (float(washout_count)/float(total_trades)) * 100
            },
            'subTrades':{
                'secondaryTradeCount': secondary_trades_count,
                'partialShipmentCount': partial_shipment_count,
                'secondaryTradePercentage': (float(secondary_trades_count)/float(total_trades)) *100
            },
            'arrivedNotCompletedCount': arrived_at_port_not_completed_count,
            'expectedArrivalCount': expected_arrival_count,
            'notShippedCount': not_shipped_count
        }

