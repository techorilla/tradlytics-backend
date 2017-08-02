from doniApi.apiImports import Response, GenericAPIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from doniServer.models import Transaction, TransactionChangeLog, ShippingPort, ShippingLine, Vessel, BpBasic, TrSellerInvoice
import dateutil.parser
from notifications.signals import notify

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
                    shipment.shipped = True
                    shipment.not_shipped = False
                else:
                    shipment.arrived_at_port = False
            else:
                raise Exception('No Status Provided!')

            shipment.save()
            txt_status = shipment_status.replace('_', ' ')
            peers = user.profile.get_notification_peers()


            if activate:
                log = self.ACTIVATED_MESSAGE%txt_status
                notification_msg = '<strong> File Id  %s</strong> %s status activated' % (transaction.file_id, txt_status)
                TransactionChangeLog.add_change_log(user, log, transaction)
                notify.send(user, recipient=peers, verb=notification_msg, description='international_trade',
                            state='dashboard.transactionView',
                            state_params={'id': transaction.file_id}, user_image=user.profile.get_profile_pic())

            else:
                log = self.DEACTIVATED_MESSAGE%txt_status
                notification_msg = '<strong> File Id  %s</strong> %s status deactivated' % (transaction.file_id, txt_status)
                TransactionChangeLog.add_change_log(user, log, transaction)
                notify.send(user, recipient=peers, verb=notification_msg, description='international_trade',
                            state='dashboard.transactionView',
                            state_params={'id': transaction.file_id}, user_image=user.profile.get_profile_pic())


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
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            transaction_id = data.get('transactionId')
            shipped_data = data.get('dataObj')
            base_url = request.META.get('HTTP_HOST')
            user = request.user
            transaction = Transaction.objects.get(tr_id=transaction_id)
            shipment = transaction.shipment
            try:
                shipper_id = shipped_data.get('shipper',{}).get('id')
            except AttributeError:
                shipper_id = None

            transit_ports = shipped_data.get('transitPorts')
            shipped_on = shipped_data.get('shippedOn')
            expected_arrival = shipped_data.get('expectedArrival')
            seller_invoice_no = shipped_data.get('sellerInvoiceNo')
            seller_invoice_amount = shipped_data.get('sellerInvoiceAmount')

            seller_invoice = None if not hasattr(transaction, 'seller_invoice') else transaction.seller_invoice

            if seller_invoice:
                TrSellerInvoice.save_seller_invoice(seller_invoice_no,seller_invoice_amount, transaction)
            else:
                if seller_invoice_no and seller_invoice_amount:
                    TrSellerInvoice.save_seller_invoice(seller_invoice_no, seller_invoice_amount, transaction)

            if shipped_on:
                shipped_on = dateutil.parser.parse(str(shipped_on).replace('"', ''))
                shipped_on = shipped_on.replace(hour=0, minute=0, second=0, microsecond=0)

            if expected_arrival:
                expected_arrival = dateutil.parser.parse(str(expected_arrival).replace('"', ''))
                expected_arrival = expected_arrival.replace(hour=0, minute=0, second=0, microsecond=0)

            shipper = None
            if shipper_id:
                shipper = BpBasic.objects.get(bp_id=shipper_id)

            shipment.transit_port = transit_ports
            shipment.date_shipped_on = shipped_on
            shipment.expected_arrival = expected_arrival
            shipment.shipper = shipper
            shipment.save()

            return Response({
                'transactionObj': transaction.get_complete_obj(base_url, user),
                'success': True,
                'message': 'Shipment Arrived At Port Information Updated!'
            })
        except Exception, e:
            import traceback
            print traceback.format_exc()
            print str(e)
            return Response({
                'success': False,
                'message': str(e)
            })



class ShipmentNotShippedInfoAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            transaction_id = data.get('transactionId')
            not_shipped_data = data.get('dataObj')
            base_url = request.META.get('HTTP_HOST')
            user = request.user
            transaction = Transaction.objects.get(tr_id=transaction_id)
            shipment = transaction.shipment
            extension_date =  not_shipped_data.get('shipmentExtension')
            if extension_date:
                extension_date = dateutil.parser.parse(str(extension_date).replace('"', ''))
                extension_date = extension_date.replace(hour=0, minute=0, second=0, microsecond=0)
            shipment.not_shipped_reason = not_shipped_data.get('reason', '')
            shipment.extension = extension_date
            shipment.save()
            return Response({
                'success': True,
                'transactionObj': transaction.get_complete_obj(base_url, user),
                'message': 'Shipment Arrived At Port Information Updated!'
            })
        except Exception, e:
            print str(e),e
            return Response({
                'success': False,
                'message': str(e)
            })



class ShipmentApprobationReceivedInfoAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            base_url = request.META.get('HTTP_HOST')
            user = request.user
            transaction_id = data.get('transactionId')
            transaction = Transaction.objects.get(tr_id=transaction_id)
            shipment = transaction.shipment

            data_obj = data.get('dataObj')
            print data_obj

            expected_shipment = data_obj.get('expectedShipment')
            in_transit = data_obj.get('inTransit')

            if expected_shipment:
                expected_shipment = dateutil.parser.parse(str(expected_shipment).replace('"', ''))
                expected_shipment = expected_shipment.replace(hour=0, minute=0, second=0, microsecond=0)

            if in_transit:
                in_transit = dateutil.parser.parse(str(in_transit).replace('"', ''))
                in_transit = in_transit.replace(hour=0, minute=0, second=0, microsecond=0)


            shipment.expected_shipment = expected_shipment
            shipment.in_transit = in_transit
            shipment.save()


            return Response({
                'success': True,
                'transactionObj': transaction.get_complete_obj(base_url, user),
                'message': 'Shipment Approbation Information Updated!'
            })
        except Exception, e:
            print str(e)
            return Response({
                'success': False,
                'message': str(e)
            })



class ShipmentArrivedAtPortInfoAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            base_url = request.META.get('HTTP_HOST')
            user = request.user
            transaction_id = data.get('transactionId')

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

            #saving shipment details
            loading_port_id = data_obj.get('loadingPort').get('id')
            shipping_line_id = data_obj.get('shippingLine').get('id')
            try:
                vessel_id = data_obj.get('vessel',[{}])[0].get('id')
            except IndexError:
                vessel_id = None
            destination_port_id = data_obj.get('destinationPort').get('id')
            bl_no = data_obj.get('blNo')
            voyage_no = data_obj.get('voyageNo')
            containers = data_obj.get('containers')


            loading_port = ShippingPort.objects.get(id=loading_port_id) if loading_port_id else None
            destination_port = ShippingPort.objects.get(id=destination_port_id) if destination_port_id else None
            shipping_line = ShippingLine.objects.get(id=shipping_line_id) if shipping_line_id else None

            vessel = Vessel.objects.get(id=vessel_id) if vessel_id else None
            shipment.bl_no = bl_no
            shipment.voyage_no = voyage_no
            shipment.containers = containers
            shipment.port_loading = loading_port
            shipment.port_destination = destination_port
            shipment.shipping_line = shipping_line
            shipment.vessel=vessel
            shipment.save()

            return Response({
                'success': True,
                'transactionObj': trade.get_complete_obj(base_url, user),
                'message': 'Shipment Arrived At Port Information Updated!'
            })
        except Exception, e:
            print str(e)
            return Response({
                'success': False,
                'message': str(e)
            })
