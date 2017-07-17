from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import Transaction, TransactionChangeLog


class TransactionShipmentStatusAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    SHIPMENT_STATUS = {
        'NOT_SHIPPED': 'NOT_SHIPPED',
        'APPROBATION_RECEIVED': 'APPROBATION_RECEIVED',
        'SHIPPED': 'SHIPPED',
        'ARRIVED_AT_PORT': 'ARRIVED_AT_PORT'
    }

    ACTIVATED_MESSAGE = '<span class="titled">%s</span> shipment status activated.'
    DEACTIVATED_MESSAGE = '<span class="titled">%s</span> shipment status deactivated.'

    def post(self, request, *args, **kwargs):
        try:
            base_url = request.META.get('HTTP_HOST')
            user = request.user

            data = request.data
            shipment_status = data.get('shipmentStatus')

            activate = data.get('status')
            transaction_id = data.get('transactionId')

            transaction = Transaction.objects.get(tr_id=transaction_id)
            shipment = transaction.shipment

            if shipment_status == self.SHIPMENT_STATUS['NOT_SHIPPED']:
                if activate:
                    shipment.not_shipped = True
                    shipment.shipped = False
                    shipment.arrived_at_port = False

                else:
                    shipment.not_shipped = False

            elif shipment_status == self.SHIPMENT_STATUS['APPROBATION_RECEIVED']:
                if activate:
                    shipment.app_received = True
                else:
                    shipment.app_received = False

            elif shipment_status == self.SHIPMENT_STATUS['SHIPPED']:
                if activate:
                    shipment.shipped = True
                    shipment.not_shipped = False
                else:
                    shipment.not_shipped = True
                    shipment.shipped = False
                    shipment.arrived_at_port = False

            elif shipment_status == self.SHIPMENT_STATUS['ARRIVED_AT_PORT']:
                if activate:
                    shipment.arrived_at_port = True
                else:
                    shipment.arrived_at_port = False
            else:
                raise Exception('No Status Provided!')

            shipment.save()
            txt_status = shipment_status.replace('_', ' ')
            if activate:
                log = self.ACTIVATED_MESSAGE%txt_status
                TransactionChangeLog.add_change_log(user, log, transaction)
            else:
                log = self.DEACTIVATED_MESSAGE%txt_status
                TransactionChangeLog.add_change_log(user, log, transaction)


            return Response({
                'transactionObj': transaction.get_complete_obj(base_url, user),
                'success': True,
                'message': 'Transaction Shipment status changed successfully'
            })


        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })


class ShipmentShippedInfoAPI(GenericAPIView):

    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            transaction_id = data.get('transactionId')
            base_url = request.META.get('HTTP_HOST')
            user = request.user
            trade = Transaction.objects.get(tr_id=transaction_id)
            shipment = trade.shipment

            return Response({
                'transactionObj': transaction.get_complete_obj(base_url, user),
                'success': True,
                'message': 'Shipment Arrived At Port Information Updated!'
            })
        except Exception, e:
            return Response({
                'success': True
            })



class ShipmentNotShippedInfoAPI(GenericAPIView):
    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            transaction_id = data.get('transactionId')
            base_url = request.META.get('HTTP_HOST')
            user = request.user
            trade = Transaction.objects.get(tr_id=transaction_id)
            shipment = trade.shipment

            return Response({
                'success': True,
                'transactionObj': transaction.get_complete_obj(base_url, user),
                'message': 'Shipment Arrived At Port Information Updated!'
            })
        except Exception, e:
            return Response({
                'success': True
            })



class ShipmentApprobationReceivedInfoAPI(GenericAPIView):
    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            base_url = request.META.get('HTTP_HOST')
            user = request.user
            transaction_id = data.get('transactionId')
            trade = Transaction.objects.get(tr_id=transaction_id)
            shipment = trade.shipment

            return Response({
                'success': True,
                'transactionObj': transaction.get_complete_obj(base_url, user),
                'message': 'Shipment Arrived At Port Information Updated!'
            })
        except Exception, e:
            return Response({
                'success': True
            })



class ShipmentArrivedAtPortInfoAPI(GenericAPIView):

    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            base_url = request.META.get('HTTP_HOST')
            user = request.user
            transaction_id = data.get('transactionId')
            print transaction_id

            data_obj = data.get('dataObj')
            trade = Transaction.objects.get(tr_id=transaction_id)

            shipment = trade.shipment
            commission = trade.commission
            #saving Shipment Data
            quantity_shipped = data_obj.get('quantityShipped')

            if quantity_shipped:
                trade.commission.quantity_shipped = float(quantity_shipped)
                shipment.save()
                commission.save()


            return Response({
                'success': True,
                'transactionObj': trade.get_complete_obj(base_url, user),
                'message': 'Shipment Arrived At Port Information Updated!'
            })
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })
