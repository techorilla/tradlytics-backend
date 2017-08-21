from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import Transaction, TradeDispute
from datetime import datetime as dt
import dateutil.parser


class TransactionDisputeAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        base_url = request.META.get('HTTP_HOST')
        user = request.user
        file_id = data.get('fileId')
        transaction = Transaction.objects.get(file_id=file_id)
        dispute_already_exist = hasattr(transaction, 'dispute')
        activate = data.get('activate')
        dispute_resolved = data.get('disputeResolved')
        other = data.get('other')
        weight_shortage = data.get('weightShortage')
        quality_complain = data.get('qualityComplain')
        details = data.get('details')
        dispute_date = data.get('disputeDate')
        dispute_resolved_date = data.get('disputeResolvedDate')

        if dispute_date:
            dispute_date = dateutil.parser.parse(str(dispute_date).replace('"', ''))
            print dispute_date.date()

        if dispute_resolved_date:
            dispute_resolved_date = dateutil.parser.parse(str(dispute_resolved_date).replace('"', ''))
            print dispute_resolved_date.date()


        if activate:
            if not dispute_already_exist:
                dispute = TradeDispute()
                dispute.transaction = transaction
                dispute.created_by = request.user

            else:
                dispute = transaction.dispute
                dispute.updated_by = request.user
                dispute.updated_at = dt.now()

            dispute.dispute_date = dispute_date
            dispute.quality_complain = quality_complain
            dispute.weight_shortage = weight_shortage
            dispute.other_complain = other
            dispute.dispute_resolved = dispute_resolved
            dispute.dispute_resolved_date = dispute_resolved_date
            dispute.details = details
            dispute.save()
            return Response({
                'transactionObj': transaction.get_complete_obj(base_url, user),
                'success': True,
                'message': 'Transaction with File Id %s dispute saved successfully' % transaction.file_id
            }, status=status.HTTP_200_OK)

        else:
            transaction.dispute.delete()
            transaction.dispute = None
            transaction.save()
            return Response({
                'transactionObj': transaction.get_complete_obj(base_url, user),
                'success': True,
                'message': 'Transaction with File Id %s dispute removed successfully' % transaction.file_id
            }, status=status.HTTP_200_OK)

    def save_trade_dispute(self, data, user):
        return None

