from django.db import models
from datetime import date
from django.contrib.auth.models import User
from .trBasic import Transaction
from ..businessPartner import BpBasic
from ..shipment import ShippingPort, ShippingLine, Vessel
from jsonfield import JSONField
from django.utils import timezone


class TrShipment(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        null=True,
        related_name='shipment'
    )

    shipper = models.ForeignKey(BpBasic, null=True, related_name='tr_shipment_shipper')

    not_shipped = models.BooleanField(default=False)
    not_shipped_reason = models.TextField(null=True)
    extension = models.DateField(default=None, null=True)
    app_received = models.BooleanField(default=False)
    expected_shipment = models.DateField(default=None, null=True)
    in_transit = models.DateField(default=None, null=True)
    shipped = models.BooleanField(default=False)
    date_arrived = models.DateField(default=None, null=True)
    expected_arrival = models.DateField(default=None, null=True)
    transit_port = JSONField(null=True)
    arrived_at_port = models.BooleanField(default=False)
    date_arrived = models.DateField(default=None, null=True)
    date_shipped_on = models.DateField(default=None, null=True)
    actual_arrived = models.DateField(default=None, null=True)
    bl_no = models.CharField(max_length=50, null=True)
    invoice_no = models.CharField(max_length=50, null=True)
    invoice_amount = models.FloatField(null=True)
    quantity = models.FloatField(null=True)
    vessel = models.ForeignKey(Vessel, null=True, related_name='tr_shipment_vessel')

    port_loading = models.ForeignKey(ShippingPort, null=True, related_name='tr_shipment_port_loading')
    port_destination = models.ForeignKey(ShippingPort, null=True, related_name='tr_shipment_port_destination')
    shipping_line = models.ForeignKey(ShippingLine, null=True, related_name='line_shipments')
    chk_reason = models.BooleanField(default=False)
    chk_ship_ext = models.BooleanField(default=False)
    chk_exp_ship = models.BooleanField(default=False)
    chk_in_transit = models.BooleanField(default=False)
    chk_date_shipped = models.BooleanField(default=False)
    chk_expected_arrival = models.BooleanField(default=False)
    chk_transit_port = models.BooleanField(default=False)
    chk_date_arrived = models.BooleanField(default=False)
    chk_actual_arrived = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
    created_by = models.ForeignKey(User, null=False, blank=False, related_name='tr_shipment_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=False, related_name='tr_shipment_updated_by')

    class Meta:
        db_table = 'tr_shipment'


    def get_description_object(self, base_url):
        seller_invoice = None if not hasattr(self.transaction, 'seller_invoice') else self.transaction.seller_invoice

        return {
            'notShipped': {
                'active': self.not_shipped,
                'reason': None if not self.not_shipped_reason else self.not_shipped_reason,
                'shipmentExtension': None if not self.extension else self.extension

            },
            'approbationReceived':{
                'active': self.app_received,
                'expectedShipment': self.expected_shipment,
                'inTransit': self.in_transit,
            },
            'shipped':{
                'active': self.shipped,
                'expectedArrival': self.expected_arrival,
                'sellerInvoiceNo': None if not seller_invoice else seller_invoice.tr_seller_invoice_no,
                'sellerInvoiceAmount': None if not seller_invoice else seller_invoice.tr_seller_invoice_amount_usd,
                'shipper': None if not self.shipper else self.shipper.get_description_obj(base_url),
                'shippedOn': self.date_shipped_on,
                'transitPorts': [] if not self.transit_port else self.transit_port

            },
            'arrivedAtPort':{
                'vessel': [] if not self .vessel else [self.vessel.get_tag_obj()],
                'active': self.arrived_at_port,
                'quantityShipped': None if not self.transaction.commission.quantity_shipped else str(round(self.transaction.commission.quantity_shipped,2)),
                'blNo': self.bl_no,
                'shippingLine': {} if not self.shipping_line else self.shipping_line.get_drop_down_obj(),
                'loadingPort': {} if not self.port_loading else self.port_loading.get_drop_down_obj(),
                'destinationPort': {} if not self.port_destination else self.port_destination.get_drop_down_obj()
            }
        }


